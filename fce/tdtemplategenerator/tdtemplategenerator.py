import os
import FreeCAD


class TDTemplateGenerator:
    """
    Writes custom SVG files to be used as TechDraw Templates.

    Parameters
    ----------
    template_name: str
        Name of template file.
    width: str
        Number that represents width of SVG file.
    height: str
        Number that represents height of SVG file.
    margin: str
        Number that represents margin of inner border.
    font_size: str
        Number that represents font size of text.
    units: str
        Units of SVG dimensions.
    indent_factor: int
        Number of spaces when indentating.
    """
    def __init__(
            self,
            template_name="UntitledTechDraw",
            width="11",
            height="8.5",
            margin="0.25",
            font_size="0.15",
            units="in",
            indent_factor=2
    ):
        # Retrieving file address information
        self._parameter_path = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Files")
        self._template_path = self._parameter_path.GetString("TemplateDir")
        self._template_name = template_name + ".svg"
        self._template_file = os.path.join(self._template_path, self._template_name)
        # Instantiating variables
        self.units = units
        self.page_width = width
        self.page_height = height
        self.margin = margin
        self.font_size = font_size
        self.indent_factor = indent_factor
        self.indent_level = 0
        # Writing Metadata
        self._t = open(self._template_file, "w", encoding="utf-8")
        self.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
        self._t.close()
        # Writing SVG attributes
        self._t = open(self._template_file, "a", encoding="utf-8")
        self.write("<svg")
        self.indent_level += 1
        self.write("xmlns=\"http://www.w3.org/2000/svg\"")
        self.write("version=\"1.1\"")
        self.write(
            "xmlns:freecad=\"http://www.freecadweb.org/wiki/index.php?title=Svg_Namespace\""
        )
        self.write(f"width =\"{self._to_mm(self.page_width)}mm \"")
        self.write(f"height =\"{self._to_mm(self.page_height)}mm \"")
        self.write(f"viewBox=\"0 0 {self._to_mm(self.page_width)} {self._to_mm(self.page_height)}\"")
        self.indent_level -= 1
        self.write(">")
        self.indent_level += 1
        return

    def write(self, text):
        """
        Absctration of file writing that automatically adds indent spacing.

        Paramters
        ---------
        text: str
            Text to write into SVG file
        """
        indentation = self.indent_level*self.indent_factor*' '
        self._t.write(f"{indentation}{text}\n")
        return

    def _to_mm(self, number):
        """
        Converts numerical value to millimeters.
        To add editable text in FreeCAD, all numbers must be in mm.

        Parameters
        ----------
        number: str, int, float
            Numerical value in not in millimeters.

        Returns
        -------
        str
            Numerical value in millimeters.
        """
        if number not in {"v", "V", "h", "H"}:
            if type(number) == str:
                number = float(number)
            if self.units == "in":
                number *= 25.4
        return str(number)

    def _svg_path(self, x1, y1, x2, y2):
        """
        Contructs <path> SVG element from two (x,y) coordinates, or, one coordinate and one length.

        Parameters
        ----------
        x1: str
            Number that represent the x-coorinate of the start point.
        y1: str
            Number that represent the y-coorinate of the start point.
        x2: str
            Number that represent the x-coorinate of the end point.
            If set to a v or h letter, the path will be a vertical or horizontal line from start point.
        y2: str
            Number that represent the x-coorinate of the end point, or, length of the line.

        Returns
        -------
        str
            <path> SVG element.
        """
        x1 = self._to_mm(x1)
        y1 = self._to_mm(y1)
        x2 = self._to_mm(x2)
        y2 = self._to_mm(y2)
        if x2 in {"v", "V", "h", "H"}:
            return f"<path d=\"m {x1},{y1} {x2} {y2}\" />"
        else:
            return f"<path d=\"m {x1},{y1} l {x2},{y2}\" />"

    def _svg_rect(self, width, height, x, y):
        """
        Constructs <rect> SVG element from an (x,y) coordinate, width, and height.

        Parameters
        ----------
        x: str
            Number that represents x-coordinate of starting point.
        y: str
            Number that represents y-coordinate of starting point.
        width: str
            Number that represents rectangle width extending through x+.
        height: str
            Number that represents rectangle height extending through y+.

        Returns
        -------
        str
            <rect> SVG element.
        """
        x = self._to_mm(x)
        y = self._to_mm(y)
        width = self._to_mm(width)
        height = self._to_mm(height)
        return f"<rect width=\"{width}\" height=\"{height}\" x=\"{x}\" y=\"{y}\" />"

    def _svg_text(self, text, x, y):
        """
        Constructs <text> SVG element.

        Parameters
        ----------
        text: str
            Text for <text> SVG element.
        x: str
            Number that represents x-coordinate of starting point.
        y: str
            Number that represents y-coordinate of starting point.

        Returns
        -------
        str
            <path> SVG element
        """
        x = self._to_mm(x)
        y = self._to_mm(y)
        return f"<text x=\"{x}\" y=\"{y}\">{text}</text>"

    def _svg_text_editable(self, text, x, y, identifier):
        """
        Constructs <text> SVG element that is editable through FreeCAD.

        Parameters
        ----------
        text: str
            Text for <text> SVG element.
        x: str
            Number that represents x-coordinate of starting point.
        y: str
            Number that represents y-coordinate of starting point.

        Returns
        -------
        str
            <path> SVG element
        """
        x = self._to_mm(x)
        y = self._to_mm(y)
        return f"<text freecad:editable=\"{identifier}\" x=\"{x}\" y=\"{y}\">  <tspan>{text}</tspan>  </text>"

    def start_graphic(self, identifier, style="", transform=""):
        """
        Initiates <g> SVG element writing.

        Parameters
        ----------
        identifier: str
            Element ID for documentation purposes.
        style: str
            Styling attributes for elements within <g>.
        transform:
            Transformation attributes for elements within <g>.
        """
        self.write("<g")
        self.indent_level += 1
        self.write(f"id=\"{identifier}\"")
        if style != "":
            self.write(f"style=\"{style}\"")
        if transform != "":
            self.write(f"transform=\"{transform}\"")
        self.indent_level += -1
        self.write(">")
        self.indent_level += 1
        return

    def add_graphic(self, svg_type, params: list):
        """
        Adds specified SVG element within current <g> SVG element.
        Requires tdtemplategenerator.start_graphic() to be called before usage.

        Parameters
        ---------
        svg_type: str
            SVG element to render.
            May only be 'rect', 'path', 'text', or 'text_editable'.
        params: str
            Parameters for rendering the SVG element (see above SVG construction methods).
        """
        if svg_type == "rect":
            self.write(self._svg_rect(*params))
        elif svg_type == "path":
            self.write(self._svg_path(*params))
        elif svg_type == "text":
            self.write(self._svg_text(*params))
        elif svg_type == "text_editable":
            self.write(self._svg_text_editable(*params))
        return

    def end_graphic(self):
        """
        Closes <g> SVG element writing for current <g>.
        """
        self.indent_level -= 1
        self.write("</g>")
        return

    def close_svg(self):
        """
        Closes SVG writing.
        Must be executed at final step of SVG writing.
        """
        self.indent_level = 0
        self.write("</svg>")
        self._t.close()
        return

    def create_frame(self):
        """
        Draws inner border around SVG.
        """
        self.start_graphic(
            "frame-border",
            "fill:none;stroke:#000000;stroke-width:0.25;stroke-linecap:round"
        )
        self.add_graphic(
            "rect",
            [
                str(float(self.page_width) - 2 * float(self.margin)),
                str(float(self.page_height) - 2 * float(self.margin)),
                self.margin,
                self.margin
            ]
        )
        self.end_graphic()
        return
