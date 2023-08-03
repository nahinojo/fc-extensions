import string
from mfl.tdtemplategenerator.tdtemplategenerator import TDTemplateGenerator


class TDTemplateGeneratorPrime(TDTemplateGenerator):

    def __init__(self, *args):
        super().__init__(*args)
        return

    def _create_frame_datum_symbols(self, x_datum_count: int, y_datum_count: int):
        """
        Places datums symbols along the edges of the frame.

        Parameters
        ----------
            x_datum_count: int
                Number of datum symbols to place along x-axis
            y_datum_count: int
                Number of datum symbols to places along y-axis
        """
        styling_normal = "font-size:4;text-anchor:middle;fill:#000000;font-family:osifont;"
        styling_rotated = f"{styling_normal}transform:translate(0,0) rotate(270)"
        # Setting x-datums
        #
        # Determining x-datums
        x_datums = []
        for idx in range(x_datum_count):
            x_datums.append(string.ascii_uppercase[idx])
        x_datums.reverse()
        # Calculating x-datums locations
        x_length = float(self.page_width)
        x_diff = x_length / x_datum_count
        x_loc_init = .5 * x_diff - .5 * float(self.font_size)
        # Writing x-datums along upper page edge.
        x_loc_current = x_loc_init + .5 * float(self.margin)
        for idx in range(x_datum_count):
            y_loc = .25 * float(self.margin)
            self.start_graphic(
                "frame-datums",
                styling_rotated
            )
            self.add_graphic("text", [x_datums[idx], str(-y_loc), str(x_loc_current)])
            self.end_graphic()
            x_loc_current += x_diff
        # Writing x-datums along lower page edge.
        x_loc_current = .5 * x_diff
        for idx in range(x_datum_count):
            y_loc = float(self.page_height) - 0.0625 * float(self.margin)
            self.start_graphic(
                "frame-datums",
                styling_normal
            )
            self.add_graphic("text", [x_datums[idx], str(x_loc_current), str(y_loc)])
            self.end_graphic()
            x_loc_current += x_diff
        # Setting y-datums.
        #
        # Determining y-datums.
        y_datums = []
        for idx in range(y_datum_count):
            y_datums.append(str(idx + 1))
        y_datums.reverse()
        # Calculating y-datums locations.
        y_length = float(self.page_height)
        y_diff = y_length / y_datum_count
        y_loc_init = 0.5 * y_diff
        # Writing y-datums to right page edge
        x_loc = float(self.page_width) - 0.25 * float(self.margin)
        y_loc_current = y_loc_init + float(self.font_size)
        for idx in range(y_datum_count):
            self.start_graphic(
                "frame-datums",
                styling_normal
            )
            self.add_graphic("text", [y_datums[idx], str(x_loc), str(y_loc_current)])
            self.end_graphic()
            y_loc_current += y_diff
        # Writing y-datums on left page edge
        y_loc_current = y_loc_init
        x_loc = .5 * float(self.margin)
        for idx in range(y_datum_count):
            self.start_graphic(
                "frame-datums",
                styling_rotated
            )
            self.add_graphic("text", [y_datums[idx], str(-y_loc_current), str(x_loc)])
            self.end_graphic()
            y_loc_current += y_diff
        return

    def _create_frame_ticks(self, x_datum_count, y_datum_count):
        """
        Places datum ticks along edges of frame

        Parameters
        ----------
            x_datum_count: int
                Number of datum symbols to place along x-axis
            y_datum_count: int
                Number of datum symbols to places along y-axis
        """
        # Writing ticks along upper and lower edges
        x_diff = float(self.page_width) / x_datum_count
        x_loc_current = x_diff
        styling = "fill:none;stroke:#000000;stroke-width:0.25;stroke-linecap:round"
        for idx in range(x_datum_count - 1):
            self.start_graphic(
                "frame-ticks",
                styling
            )
            coords = [
                str(x_loc_current),
                str(.5 * float(self.margin)),
                'v',
                str(.5 * float(self.margin))
            ]
            self.add_graphic(
                "path",
                coords
            )
            coords[1] = str(float(self.page_height) - float(self.margin))
            self.add_graphic(
                "path",
                coords
            )
            self.end_graphic()
            x_loc_current += x_diff
        # Writing ticks along right and left edges
        y_diff = float(self.page_height) / y_datum_count
        y_loc_current = y_diff
        for idx in range(y_datum_count - 1):
            self.start_graphic(
                "frame-ticks",
                styling
            )
            coords = [
                str(.5 * float(self.margin)),
                str(y_loc_current),
                'h',
                str(.5 * float(self.margin))
            ]
            self.add_graphic(
                "path",
                coords
            )
            coords[0] = str(float(self.page_width) - float(self.margin))
            self.add_graphic(
                "path",
                coords
            )
            self.end_graphic()
            y_loc_current += y_diff
        return

    def create_frame_datums(self, x_datum_count, y_datum_count):
        """
        Adds datums and ticks along edges of SVG
        """
        self._create_frame_datum_symbols(x_datum_count, y_datum_count)
        self._create_frame_ticks(x_datum_count, y_datum_count)
        return


# Main program
if __name__ == "__main__":
    # Document dimensions (inches)
    format_width = "11"
    format_height = "8.5"
    format_margin = "0.25"
    format_font_size = ".15"
    X_datum_count = 6
    Y_datum_count = 4

    # Initialization
    nhdraw = TDTemplateGeneratorPrime(
        "ReduxDrawing3",
        format_width,
        format_height,
        format_margin,
        format_font_size
    )
    styling_lines = "fill:none;stroke:#000000;stroke-width:0.25;stroke-linecap:round"
    styling_text_left = "font-size:2.5;text-anchor:start;fill:#000000;font-family:osifont;"
    styling_text_middle = "font-size:2.5;text-anchor:middle;fill:#000000;font-family:osifont;"
    nhdraw.create_frame()
    nhdraw.create_frame_datums(X_datum_count, Y_datum_count)
    nhdraw.start_graphic(
        "boxes",
        styling_lines
    )
    # Adding major horizontal paths
    path_coords = [
        ["5.5", "5.75", "h", "5.25"],
        ["5.5", "6.25", "h", "5.25"],
        ["5.5", "6.75", "h", "5.25"],
    ]
    # Adding minor horizontal paths
    path_h_curr = ["9.5", "5.75", "h", "1.25"]
    for path_h_idx in range(9):
        path_h_curr[1] = str(float(path_h_curr[1]) + .25)
        if path_h_idx in {1, 3}:
            continue
        path_coords.append(path_h_curr.copy())
    path_coords.append(["5.5", "7.75", "h", "1.25"])
    # Adding major vertical paths
    path_coords.append(["5.5", "5.75", "v", "2.5"])
    path_coords.append(["6.75", "5.75", "v", "2.5"])
    path_coords.append(["8", "5.75", "v", "2.5"])
    path_coords.append(["9.5", "5.75", "v", "2.5"])
    path_coords.append(["9.75", "5.75", "v", "2.5"])
    # Adding minor vertical paths
    path_coords.append(["6.125", "6.25", "v", "0.5"])
    path_coords.append(["6.125", "7.75", "v", "0.5"])
    # Writing paths to SVG
    for coord in path_coords:
        nhdraw.add_graphic(
            "path",
            coord
        )
    nhdraw.end_graphic()

    # Adding attribute title text
    def add_text(text_label, x_loc, y_loc):
        nhdraw.add_graphic("text", [text_label, str(x_loc), str(y_loc)])


    nhdraw.start_graphic(
        "titles",
        styling_text_left
    )
    # Adding top row titles
    text_params = ["Title:", "5.5625", "5.875"]
    text_labels = ["Date:", "Author:"]
    label = text_params[0]
    x = float(text_params[1])
    y = float(text_params[2])
    add_text(label, x, y)
    for i in range(len(text_labels)):
        label = text_labels[i]
        x += 1.25
        add_text(label, x, y)
    # Adding second top row titles
    text_params = ["Size:", "5.5625", "6.375"]
    text_labels = ["Scale:", "Approver:"]
    label = text_params[0]
    x = float(text_params[1])
    y = float(text_params[2])
    add_text(label, x, y)
    for i in range(len(text_labels)):
        label = text_labels[i]
        if i == 0:
            x += 1.25 * .5
        else:
            x += 1.25 * 1.5
        add_text(label, x, y)
    # Adding remaining left column titles
    text_params = ["Drawing Number:", "5.5625", "6.875"]
    text_labels = ["Part Number:", "Sheet:"]
    label = text_params[0]
    x = float(text_params[1])
    y = float(text_params[2])
    add_text(label, x, y)
    for i in range(len(text_labels)):
        label = text_labels[i]
        y += .5
        add_text(label, x, y)
    # Adding final titles
    label = "Revision:"
    x += 1.25 / 2
    add_text(label, x, y)
    label = "Supplemental Information:"
    x = 5.5625 + 1.25 + 1.25
    y = 5.875 + .5 + .5
    add_text(label, x, y)
    nhdraw.end_graphic()
    # Adding column of letters to variable box
    nhdraw.start_graphic(
        "letters",
        styling_text_middle
    )
    letters = []
    for i in range(10):
        letters.append(string.ascii_uppercase[i])
    letters.reverse()
    x = 9.625
    y = 5.912 - .25
    label = letters[0]
    for i in range(len(letters)):
        y += .25
        label = letters[i]
        add_text(label, x, y)
    nhdraw.end_graphic()

    # Adding editable text
    def add_text_editable(label_t, x_t, y_t, identifier_t):
        nhdraw.add_graphic(
            "text_editable",
            [label_t, str(x_t), str(y_t), identifier_t]
        )


    styling_text_editable_left = \
        "font-size:4;text-anchor:start;dominant-baseline:middle;fill:#000000;font-family:osifont;"
    nhdraw.start_graphic(
        "editable_text",
        styling_text_editable_left
    )
    label = ""
    x = 5.625
    y = 6.125
    identifier = "Title"
    identifier_list = ["Date", "Author"]
    add_text_editable(label, x, y, identifier)
    for i in range(2):
        x += 1.25
        identifier = identifier_list[i]
        add_text_editable(label, x, y, identifier)
    y += .5
    identifier = "Approver"
    add_text_editable(label, x, y, identifier)
    x = 5.625
    y = 6.125 + .5 * 2
    identifier = "Drawing Number"
    add_text_editable(label, x, y, identifier)
    y += .5
    identifier = "Part number"
    add_text_editable(label, x, y, identifier)
    y += .5
    identifier = "Sheet"
    add_text_editable(label, x, y, identifier)
    x += 1.25 / 2
    identifier = "Revision"
    add_text_editable(label, x, y, identifier)
    y -= .5 * 3
    x = 5.5 + 1.2 * .66666
    label = "1 : 1"
    identifier = "Scale"
    add_text_editable(label, x, y, identifier)
    nhdraw.end_graphic()
    styling_text_editable_middle_large = "font-size:7;text-anchor:middle;fill:#000000;font-family:osifont;"
    nhdraw.start_graphic(
        "editable_text_large",
        styling_text_editable_middle_large
    )
    label = "A"
    x = 5.87
    y = 6.125 + .525
    identifier = "Size"
    add_text_editable(label, x, y, identifier)
    nhdraw.end_graphic()
    styling_text_left_small = "font-size:3;text-anchor:start;fill:#000000;font-family:osifont;"
    nhdraw.start_graphic(
        "editable_text_small",
        styling_text_left_small
    )
    x = 5.625 + 1.25
    y = 6.125 + .3125
    label = "Dimensions are in"
    identifier = "Dan"
    add_text_editable(label, x, y, identifier)
    y = 6.125 + .525
    identifier = "Units"
    label = "inches and degrees"
    add_text_editable(label, x, y, identifier)
    nhdraw.end_graphic()
    styling_text_tolerance = "font-size:2.5;text-anchor:start;fill:#000000;font-family:osifont;"
    nhdraw.start_graphic(
        "editable_text",
        styling_text_tolerance
    )
    y = 6.875
    label = "Linear Toleance:"
    identifier = "Linear Tolerance"
    add_text_editable(label, x, y, identifier)
    y += .25
    label = ""
    identifier = "ltol1"
    add_text_editable(label, x, y, identifier)
    y += .25
    identifier = "ltol2"
    add_text_editable(label, x, y, identifier)
    y += .25
    label = "Angular Tolerance:"
    identifier = "Angular Tolerance"
    add_text_editable(label, x, y, identifier)
    y += .25
    label = ""
    identifier = "atol1"
    add_text_editable(label, x, y, identifier)
    y += .25
    identifier = "atol2"
    add_text_editable(label, x, y, identifier)
    x += 1.25
    y = 6.875 + .25
    label = ""
    identifier = "si1"
    add_text_editable(label, x, y, identifier)
    for i in range(4):
        y += .25
        identifier = f"si{i + 1}"
        add_text_editable(label, x, y, identifier)
    x = 9.875
    y = 5.912
    identifier = "J"
    add_text_editable(label, x, y, identifier)
    letters = []
    for i in range(9):
        letters.append(string.ascii_uppercase[i])
    letters.reverse()
    for i in range(9):
        y += .25
        identifier = letters[i]
        add_text_editable(label, x, y, identifier)
    nhdraw.end_graphic()

    nhdraw.close_svg()
