from office365.runtime.client_object import ClientObject
from office365.runtime.client_query import ClientQuery
from office365.runtime.odata.odata_path_parser import ODataPathParser
from office365.runtime.resource_path_entry import ResourcePathEntry
from office365.sharepoint.securable_object import SecurableObject


class ListItem(SecurableObject):
    """ListItem client object resource"""

    def update(self):
        """Update the list."""
        qry = ClientQuery.update_entry_query(self)
        self.context.add_query(qry)

    def delete_object(self):
        """Deletes the list."""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)

    @property
    def resource_path(self):
        orig_path = ClientObject.resource_path.fget(self)
        if self.is_property_available("Id") and "ParentList" in self.properties and orig_path is None:
            parent_list = self.properties["ParentList"]
            if '__deferred' in parent_list:
                list_resource_path = ResourcePathEntry.from_uri(self.properties["ParentList"]['__deferred']['uri'],
                                                                self.context)
            else:
                list_resource_path = parent_list.resource_path
            return ResourcePathEntry(self.context,
                                     list_resource_path,
                                     ODataPathParser.from_method("getItemById", [self.properties["Id"]]))
        return orig_path

    @property
    def file(self):
        """Get file"""
        if self.is_property_available("File"):
            return self.properties["File"]
        else:
            from office365.sharepoint.file import File
            return File(self.context, ResourcePathEntry(self.context, self.resource_path, "File"))

    @property
    def folder(self):
        """Get folder"""
        if self.is_property_available("Folder"):
            return self.properties["Folder"]
        else:
            from office365.sharepoint.folder import Folder
            return Folder(self.context, ResourcePathEntry(self.context, self.resource_path, "Folder"))

    @property
    def attachment_files(self):
        """Get attachment files"""
        if self.is_property_available('AttachmentFiles'):
            return self.properties["AttachmentFiles"]
        else:
            from office365.sharepoint.attachmentfile_collection import AttachmentfileCollection
            return AttachmentfileCollection(self.context,
                                            ResourcePathEntry(self.context, self.resource_path, "AttachmentFiles"))
