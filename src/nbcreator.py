"""
http://nbformat.readthedocs.io/en/latest/format_description.html
"""

import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell, new_raw_cell
from nbformat.notebooknode import NotebookNode


class NotebookDocument(object):

    EXT = '.ipynb'

    def __init__(self):
        self._notebook = new_notebook()
    
    def __setitem__(self, key, value):
        self._notebook[key] = value

    def __getitem__(self, item):
        return self._notebook.get(item)
    
    def add_cell(self, cell):
        if isinstance(cell, NotebookNode):
            self._notebook['cells'].append(cell)
        elif isinstance(cell, _AbstractCell):
            self._notebook['cells'].append(cell.get_cell())
        else:
            raise ValueError()

    def save_notebook(self, path, add_ext=False):
            if add_ext:
                path += self.EXT
            try:
                nbformat.write(self._notebook, path)
                return True
            except IOError('Error creating the document'):
                return False


class _AbstractCell(object):

    def __init__(self, cell_type='code', content=''):
        if cell_type == 'code':
            self._cell = new_code_cell(str(content))
        elif cell_type == 'markdown':
            self._cell = new_markdown_cell(str(content))
        elif cell_type == 'raw':
            self._cell = new_raw_cell(str(content))
        else:
            raise ValueError("Unrecognized cell type: {}" % cell_type)

    def __setitem__(self, key, value):
        self._cell[key] = value

    def __getitem__(self, item):
        return self._cell.get(item)

    def add_line(self, line):
        self._cell['source'] += str(line) + '\n'

    def get_cell(self):
        return self._cell


class CodeCell(_AbstractCell):
    """
    Clase que contiene una celda de codigo
    """
    def __init__(self, content=''):
        super(CodeCell, self).__init__('code', content)


class MarkdownCell(_AbstractCell):
    """
    Clase que contiene una celda markdown
    """
    def __init__(self, content=''):
        super(MarkdownCell, self).__init__('markdown', content)


class RawCell(_AbstractCell):
    """
    Clase que contiene una celda raw
    """
    def __init__(self, content=''):
        super(RawCell, self).__init__('raw', content)


def __example():
    # Cell 0
    markdown_cell = MarkdownCell()
    markdown_cell.add_line('This is a nbcreator test')
    # Cell 1
    code_cell_0 = CodeCell()
    code_cell_0.add_line('import numpy as np')
    code_cell_0.add_line('m0 = np.matrix([[1, 2], [3, 4]])')
    code_cell_0.add_line('m1 = np.matrix([[4, 3], [2, 1]])')

    # Cell 2
    code_cell_1 = CodeCell()
    code_cell_1.add_line('m0_mul_m1 = m0 * m1')
    code_cell_1.add_line('print(\'Result {}\'.format(m0_mul_m1))')

    # Document
    notebook = NotebookDocument()
    notebook.add_cell(markdown_cell)
    notebook.add_cell(code_cell_0)
    notebook.add_cell(code_cell_1)

    if notebook.save_notebook('test', True):
        print('Saved')
    else:
        print('IO Error')


