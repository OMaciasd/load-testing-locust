import reportlab
import chardet
import PIL
from PIL import Image

print("ReportLab version:", reportlab.Version)
print("Chardet version:", chardet.__version__)
print("Pillow version:", PIL.__version__)
print("Pillow formats:", PIL.Image.registered_extensions())

colors = [
    "red", "green", "blue", "black",
    "white", "yellow", "cyan", "magenta",
    "gray", "maroon", "olive", "lime",
    "navy", "teal", "aqua", "fuchsia",
    "beige", "ivory", "khaki", "azure",
    "lavender", "coral", "salmon", "sienna",
    "indigo", "crimson", "plum", "orchid",
    "skyblue", "tan", "wheat", "mint",
    "honeydew", "aliceblue", "ghostwhite", "linen",
    "oldlace", "powderblue", "seashell", "antiquewhite",
    "blanchedalmond", "bisque", "peachpuff", "navajowhite",
    "moccasin", "cornsilk", "lightgoldenrodyellow", "papayawhip",
    "mistyrose", "lavenderblush", "seashell", "lemonchiffon",
    "lightcyan", "lightgrey", "lightpink", "lightsalmon",
    "lightseagreen", "lightskyblue",
    "lightsteelblue", "lightyellow",
    "mediumaquamarine", "mediumseagreen", "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise", "mediumvioletred", "midnightblue",
    "mintcream",
    "mistyrose", "moccasin", "navajowhite", "oldlace",
    "olivedrab", "orange", "orangered", "orchid",
    "palegoldenrod", "palegreen", "paleturquoise",
    "palevioletred",
    "papayawhip", "peachpuff", "peru", "pink",
    "plum", "powderblue", "purple", "red",
    "rosybrown", "royalblue", "saddlebrown", "salmon",
    "sandybrown", "seagreen", "seashell", "sienna",
    "gray", "orange", "brown", "pink",
    "purple", "violet", "turquoise", "gold",
    "silver", "maroon", "olive", "lime",
    "navy", "teal", "aqua", "fuchsia",
    "silver", "gray", "maroon", "olive",
    "lime", "aqua", "teal", "navy",
    "fuchsia", "purple", "orange", "brown",
    "pink", "turquoise", "violet", "gold",
    "silver", "maroon", "olive", "lime",
    "navy", "teal", "aqua", "fuchsia",
    "beige", "ivory", "khaki", "azure",
    "lavender", "coral", "salmon", "sienna",
    "indigo", "crimson", "plum", "orchid",
    "skyblue", "tan", "wheat", "mint",
    "honeydew", "aliceblue", "ghostwhite", "linen",
    "oldlace", "powderblue", "seashell", "antiquewhite",
    "blanchedalmond", "bisque", "peachpuff", "navajowhite",
    "moccasin", "cornsilk", "lightgoldenrodyellow", "papayawhip",
    "mistyrose", "lavenderblush", "seashell", "lemonchiffon",
    "lightcyan", "lightgrey", "lightpink", "lightsalmon",
    "lightseagreen", "lightskyblue",
    "lightsteelblue", "lightyellow",
    "mediumaquamarine", "mediumseagreen", "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise", "mediumvioletred", "midnightblue",
    "mintcream",
    "mistyrose", "moccasin", "navajowhite", "oldlace",
    "olivedrab", "orange", "orangered", "orchid",
    "palegoldenrod", "palegreen", "paleturquoise",
    "palevioletred",
    "papayawhip", "peachpuff", "peru", "pink",
    "plum", "powderblue", "purple", "red",
    "rosybrown", "royalblue", "saddlebrown", "salmon",
    "sandybrown", "seagreen", "seashell", "sienna",
    "gray", "orange", "brown", "pink",
    "purple", "violet", "turquoise", "gold",
    "silver", "maroon", "olive", "lime",
    "navy", "teal", "aqua", "fuchsia",
    "beige", "ivory", "khaki", "azure",
    "lavender", "coral", "salmon", "sienna",
    "indigo", "crimson", "plum", "orchid",
    "skyblue", "tan", "wheat", "mint",
    "honeydew", "aliceblue", "ghostwhite", "linen",
    "oldlace", "powderblue", "seashell", "antiquewhite",
    "blanchedalmond", "bisque", "peachpuff", "navajowhite",
    "moccasin", "cornsilk", "lightgoldenrodyellow", "papayawhip",
    "mistyrose", "lavenderblush", "seashell", "lemonchiffon",
    "lightcyan", "lightgrey", "lightpink", "lightsalmon",
    "lightseagreen", "lightskyblue",
    "lightsteelblue", "lightyellow",
    "mediumaquamarine", "mediumseagreen", "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise", "mediumvioletred", "midnightblue",
    "mintcream",
    "mistyrose", "moccasin", "navajowhite", "oldlace",
    "olivedrab", "orange", "orangered", "orchid",
    "palegoldenrod", "palegreen", "paleturquoise",
    "palevioletred",
    "papayawhip", "peachpuff", "peru", "pink",
    "plum", "powderblue", "purple", "red",
    "rosybrown", "royalblue", "saddlebrown", "salmon",
    "sandybrown", "seagreen", "seashell", "sienna",
    "silver", "skyblue", "slateblue", "slategray",
    "slategrey", "snow", "springgreen", "steelblue",
    "tan", "teal", "thistle", "tomato"
]

# Lista de formatos compatibles con PIL
formats = ["jpg", "png", "tiff", "webp", "ppm", "pgm", "pbm",
           "pcx", "tga", "eps", "pdf", "ico"]

for color in colors:
    img = Image.new('RGB', (100, 100), color=color)

    for fmt in formats:
        filename = f"test_image_{color}.{fmt}"
        try:
            img.save(filename)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")
