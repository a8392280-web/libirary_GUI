from PySide6.QtCore import QSortFilterProxyModel, Qt

class MultiFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        # 1. Get the search pattern (what the user typed)
        regex = self.filterRegularExpression()
        
        # 2. Access the original model data
        model = self.sourceModel()
        source_index = model.index(source_row, 0, source_parent)
        
        # 3. Pull the specific data roles we want to check
        title = str(model.data(source_index, Qt.UserRole + 1) or "")
        release_date = str(model.data(source_index, Qt.UserRole + 2) or "")
        
        # 4. Return True if the search text matches EITHER field
        return (regex.match(title).hasMatch() or 
                regex.match(release_date).hasMatch())