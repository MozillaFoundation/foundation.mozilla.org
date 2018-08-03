from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    def isfile(self, name):
        return self.exists(name) and self.size(name) > 0

    def isdir(self, name):
        if not name:
            return True

        if self.isfile(name):
            return False

        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.objects.filter(Prefix=self._encode_name(name))

        for item in dirlist:
            return True
        return False

    def move(self, old_file_name, new_file_name, allow_overwrite=False):

        format_string = """
            The destination file '%s' exists and allow_overwrite is False
        """

        if self.exists(new_file_name):
            if allow_overwrite:
                self.delete(new_file_name)
            else:
                raise format_string % new_file_name

        old_key_name = self._encode_name(
            self._normalize_name(self._clean_name(old_file_name))
        )
        new_key_name = self._encode_name(
            self._normalize_name(self._clean_name(new_file_name))
        )

        k = self.bucket.copy_key(new_key_name, self.bucket.name, old_key_name)

        if not k:
            raise "Couldn't copy '%s' to '%s'" % (old_file_name, new_file_name)

        self.delete(old_file_name)

    def makedirs(self, name):
        self.save(name + "/.folder", ContentFile(""))

    def rmtree(self, name):
        name = self._normalize_name(self._clean_name(name))
        dirlist = self.bucket.objects.filter(Prefix=self._encode_name(name))
        for item in dirlist:
            item.delete()
