from MyModule.my_module import MyModule
from tests.utils import TestUtils


class TestMyModule:
    def test_create_json(self):
        out_dir = TestUtils.create_clean_test_dir('')
        some_file = out_dir.write_file("Hello World!", 'file.txt')
        iut = MyModule(some_file)
        assert iut.read() == "Hello World!"
