import unittest
import sys
import io
from contextlib import contextmanager
from models import *
from datetime import datetime
from console import HBNBCommand


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class Test_Console(unittest.TestCase):
    """
    Test the console
    """

    def setUp(self):
        self.cli = HBNBCommand()

        test_args = {'updated_at': datetime(2021-11-13 21:45:24.249806),
                     'id': '89fb5a8e-10a4-4dfe-9252-eee921991e79',
                     'created_at': datetime(2021-11-13 21:45:24.249641),
                     'name': 'Helidah'}
        self.model = BaseModel(test_args)
        self.model.save()

    def tearDown(self):
        self.cli.do_destroy("BaseModel 89fb5a8e-10a4-4dfe-9252-eee921991e79")

    def test_quit(self):
        with self.assertRaises(SystemExit):
            self.cli.do_quit(self.cli)

    def test_show_correct(self):
        with captured_output() as (out, err):
            self.cli.do_show("BaseModel 89fb5a8e-10a4-4dfe-9252-eee921991e79")
        output = out.getvalue().strip()
        self.assertFalse("2021-11-13 21:45:24.249641" in output)
        self.assertTrue('2021-11-13 21:45:24.249641' in output)

    def test_show_error_no_args(self):
        with captured_output() as (out, err):
            self.cli.do_show('')
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_show_error_missing_arg(self):
        with captured_output() as (out, err):
            self.cli.do_show("BaseModel")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_show_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_show("Human 1234-5678-9101")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_show("89fb5a8e-10a4-4dfe-9252-eee921991e79")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_create(self):
        with captured_output() as (out, err):
            self.cli.do_create('')
        output = out.getvalue().strip()
        self.assertEqual(output, "Usage: create BaseModel")

        with captured_output() as (out, err):
            self.cli.do_create("BaseModel")
        output = out.getvalue().strip()

        with captured_output() as (out, err):
            self.cli.do_show("BaseModel {}".format(output))
        output2 = out.getvalue().strip()
        self.assertTrue(output in output2)

    def test_destroy_correct(self):
        test_args = {'updated_at': datetime(2021, 11, 14, 17, 1, 13, 727563),
                     'id': 'b7e2bf1b-c80b-47ca-92ae-1c74149323e6',
                     'created_at': datetime(2021, 11, 14, 17, 1, 13, 727393)}
        testmodel = BaseModel(test_args)
        testmodel.save()
        self.cli.do_destroy("BaseModel b7e2bf1b-c80b-47ca-92ae-1c74149323e6 ")

        with captured_output() as (out, err):
            self.cli.do_show("BaseModel b7e2bf1b-c80b-47ca-92ae-1c74149323e6 ")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_destroy_error_missing_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("BaseModel")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_destroy_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("89fb5a8e-10a4-4dfe-9252-eee921991e79")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_destroy_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("Human 89fb5a8e-10a4-4dfe-9252-eee921991e79")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("BaseModel " +
                                "b7e2bf1b-c80b-47ca-92ae-1c74149323e6")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_all_correct(self):
        test_args = {'updated_at': datetime(2021, 11, 14, 17, 1, 13, 727563),
                     'id': 'b7e2bf1b-c80b-47ca-92ae-1c74149323e6',
                     'created_at': datetime(2021, 11, 14, 17, 1, 13, 727393)}
        testmodel = BaseModel(test_args)
        testmodel.save()
        with captured_output() as (out, err):
            self.cli.do_all("")
        output = out.getvalue().strip()
        self.assertTrue("89fb5a8e-10a4-4dfe-9252-eee921991e79" in output)
        self.assertTrue("b7e2bf1b-c80b-47ca-92ae-1c74149323e6" in output)
        self.assertFalse("123-456-abc" in output)

    def test_all_correct_with_class(self):
        with captured_output() as (out, err):
            self.cli.do_all("BaseModel")
        output = out.getvalue().strip()
        self.assertTrue(len(output) > 0)
        self.assertTrue("89fb5a8e-10a4-4dfe-9252-eee921991e79" in output)

    def test_all_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_all("Human")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_correct(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel " +
                               "89fb5a8e-10a4-4dfe-9252-eee921991e79 name Hezbon")
        output = out.getvalue().strip()
        self.assertEqual(output, '')

        with captured_output() as (out, err):
            self.cli.do_show("BaseModel 89fb5a8e-10a4-4dfe-9252-eee921991e79")
        output = out.getvalue().strip()
        self.assertTrue("Hezbon" in output)
        self.assertFalse("Helidah" in output)

    def test_update_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel 123-456-abc name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_error_no_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_update_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("Human " +
                               "89fb5a8e-10a4-4dfe-9252-eee921991e79 name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_error_no_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("89fb5a8e-10a4-4dfe-9252-eee921991e79 name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_update_error_missing_value(self):
        with captured_output() as (out, err):
            self.cli.do_update("BaseModel " +
                               "89fb5a8e-10a4-4dfe-9252-eee921991e79 name")
        output = out.getvalue().strip()
        self.assertEqual(output, "** value missing **")

if __name__ == "__main__":
    unittest.main()
