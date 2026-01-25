def get_movie_by_id(data, section, movie_id):
    "ٌReturn a movie info using its section and id "
    movies = data.get(section, [])
    for movie in movies:
        if movie.get("id") == movie_id:
            return movie
    return None



def get_selected_section(combo_box):
    "Return section name in the combobox"
    index = combo_box.currentIndex()
    if index == -1:  # -1 means no selection
        return None
    text = combo_box.currentText().replace(" ", "_").lower()
    if not text:  # handle empty text too
        return None
    return text


def resize_combo_box_to_contents(combo):
    "resise the combobox to  see the full title on it"
    width = max(combo.fontMetrics().horizontalAdvance(combo.itemText(i)) for i in range(combo.count())) + 30
    combo.view().setMinimumWidth(width)


