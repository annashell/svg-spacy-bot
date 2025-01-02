from functools import cache
import cairo

import spacy


@cache
def load_model(model_type):
    return spacy.load(model_type)


def get_dependencies_for_text(text):
    """
    Makes a dictionary {Word: (Head, Dependency type)} for each sentence in the input text
    Returns a list of dictionaries
    """
    nlp = load_model("fr_core_news_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    dependencies_arr = []
    for sentence in sentences:
        # adds full sentence text with punctuation to the dictionary
        dependencies_dict = {"sent": sentence}
        sentence_ = nlp(sentence)
        for token in sentence_:
            head = token.head
            dependencies_dict[token.text] = (head, token.dep_)
        dependencies_arr.append(dependencies_dict)
    return dependencies_arr


def generate_svg_for_dep_dict(text, font_size):
    """
    Picture generation function
    :param text:
    :param font_size:
    :return: generated pictures' filenames
    """
    padding = 20
    # getting dependencies for text
    dep_arr = get_dependencies_for_text(text)
    img_file_names = []
    for i, dep in enumerate(dep_arr):
        sent = dep['sent']

        # width to height is 4:1, depends on font size and sentence length
        width = font_size * (len(sent)) // 2
        height = font_size * (len(sent)) // 8

        filename = f"SVG_{i}"

        # Used the cairo lib to construct svg
        with cairo.SVGSurface(f"{filename}.svg", width, height) as surface:
            # creating a cairo context object
            context = cairo.Context(surface)

            # sentence text params
            context.set_source_rgb(0, 0, 0)
            context.set_font_size(font_size)
            context.select_font_face(
                "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            context.move_to(padding, padding)
            context.show_text(sent)

            # drawing curves for dependencies
            for key, child in dep.items():
                if key in ("sent . , : ! ; ?").split():
                    continue
                if child[0].text == key:
                    continue

                # head and child positions in text
                word_pos = sent.index(key)
                child_pos = sent.index(child[0].text)

                # drawing the curve
                # all the magic numbers were found experimentally
                curve_start_x = padding + (word_pos + len(key) // 2) * font_size // 2.25
                curve_start_y = font_size + 5
                curve_end_x = padding + (child_pos + len(child[0].text) // 2) * font_size // 2.25
                curve_middle_y = font_size + (abs(curve_end_x - curve_start_x)) * 0.25

                # add little squares near to the head of the curve
                context.rectangle(curve_start_x, curve_start_y, 2, 2)

                # to draw a curve move to start point, add two intermediate points and the final one
                context.move_to(curve_start_x, curve_start_y)
                context.set_source_rgb(1, 0, 0)
                context.curve_to((curve_end_x - curve_start_x) // 4 + curve_start_x, curve_middle_y,
                                 (curve_end_x - curve_start_x) * 3 // 4 + curve_start_x, curve_middle_y,
                                 curve_end_x, curve_start_y)
                # stroke out the color and width property
                context.stroke()

                # adding dependency type in black
                context.move_to((curve_end_x - curve_start_x) // 2 + curve_start_x - 15, curve_middle_y - 8)
                context.set_source_rgb(0, 0, 0)
                context.set_font_size(10)
                context.show_text(child[1])
                # stroke out the color and width property
                context.stroke()
            # Save a SVG pic as PNG
            surface.write_to_png(f'{filename}.png')
            img_file_names.append(f"{filename}.png")
    return img_file_names
