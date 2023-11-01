from collections import UserDict


class Note():
    def __init__(self, title: str, text: str, tags):
        self.title = title
        self.text = text
        self.__tags = set()
        self.tags = tags

    def add_tag(self, tags):
        new_tag = [tag for tag in tags]
        for i in new_tag:
            self.__tags.add(i)

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        if isinstance(tags, str):
            self.__tags.add(tags)
        elif isinstance(tags, list):
            for tag in tags:
                self.__tags.add(tag)


    def update_title(self, new_title):
        old_title = self.title
        self.title = new_title

        return "Title: '{0}' has been changed to '{1}'".format(old_title, new_title)

    def update_text(self, new_text):
        old_text = self.text
        self.text = new_text

        return "Text: '{0}' has been changed to '{1}'".format(old_text, new_text)

    def update_tags(self, new_tag):
        try:
            old_tag = ','.join(self.__tags)
        except TypeError:
            old_tag = 'There are no tags!'

        self.__tags = new_tag

        return "Tag: '{0}' has been changed to '{1}'".format(old_tag, new_tag)

    def __str__(self):
        return self.title

    def __repr__(self):
        title_to_str = '{}'.format(self.title)
        text_to_str = '{}'.format(self.text)
        tags_to_str = ','.join([str(tag) for tag in {self.__tags}])

        return title_to_str + text_to_str + tags_to_str


class Tag():
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, tag: str):
        if isinstance(tag, str):
            result = tag.lower().replace(" ","")
            self.__value = result

    def __str__(self):
        return self.__value

    def __repr__(self):
        return self.__value


class Notes(UserDict):
    def add_note(self, note: Note):
        if self.get(note.title):
            return '{} already exists.'.format(note.title)
        self.data[note.title] = note
        return '{} has been added to Notes successfully!'.format(note.title.title())

    def find(self, word: str):
        notes = []
        for note in self.data.values():
            if word.lower() in note.__repr__():
                notes.append(note)
            return notes
        else:
            "There is nothing!"

    def delete_note(self, word: str):
        for note in self.data.values():
            if word.lower() == note.title.lower():
                removed = note.title
        self.data.pop(removed)
        return 'Note {} has been removed'.format(self), self

    def get_all_notes(self):
        return self.data

    def to_dict(self):
        data = {}
        for note in self.data.values():
            data.update({str(note.title): {"title": note.title, "text": note.text, "tags": [str(tag) for tag in note.tags]}})
        return data

    def from_dict(self, data):
        for note in data:
            raw_note = data[note]
            self.add_note(Note(raw_note['title'], raw_note['text'], [Tag(value) for value in raw_note['tags']]))
