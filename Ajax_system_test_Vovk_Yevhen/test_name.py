import pytest

from scanner_handler import CheckQr


correct_qr_list = [('qwe', 'Red'), ('qwert', 'Green'), ('qwerrty', 'Fuzzy Wuzzy')]
wrong_qr_list = [('', None), ('q', None), ('qw', None), ('qwer', None), ('qwertyui', None)]


@pytest.fixture()
def check_qr():
    obj = CheckQr()
    return obj


class TestColorCase:

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_check_scanned_device_correct_qr(self, device_qr, check_qr, mocker):
        """
        Test to check color assignment at correct length
        """
        qr = device_qr[0]
        expected_color = device_qr[1]
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        check_qr.check_scanned_device(qr)
        assert check_qr.color == expected_color

    @pytest.mark.negative
    @pytest.mark.parametrize('device_qr', wrong_qr_list)
    def test_check_scanned_device_wrong_qr(self, device_qr, check_qr, mocker):
        """
        Test to check color assignment with wrong length
        """
        qr = device_qr[0]
        expected_color = device_qr[1]
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        check_qr.check_scanned_device(qr)
        assert check_qr.color == expected_color

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_check_scanned_device_correct_qr_and_db_exception(self, device_qr, check_qr):
        """
        Test to check color assignment with correct length and db connection error
        """
        qr = device_qr[0]
        expected_color = device_qr[1]
        with pytest.raises(ConnectionError):
            check_qr.check_scanned_device(qr)
            assert check_qr.color == expected_color

    @pytest.mark.negative
    @pytest.mark.parametrize('device_qr', wrong_qr_list)
    def test_check_scanned_device_wrong_qr(self, device_qr, check_qr):
        """
        Test to check color assignment with wrong length and db connection error
        """
        qr = device_qr[0]
        expected_color = device_qr[1]
        with pytest.raises(ConnectionError):
            check_qr.check_scanned_device(qr)
            assert check_qr.color == expected_color


class TestMessagesCase:

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_scan_check_out_list_without_error(self, device_qr, check_qr, mocker):
        """
        Test to check sending error with correct length and device in database
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        qr = device_qr[0]
        scan_check_out_list = check_qr.scan_check_out_list(qr)
        for i in scan_check_out_list:
            assert i() is None

    @pytest.mark.negative
    @pytest.mark.parametrize('device_qr', wrong_qr_list)
    def test_scan_check_out_list_with_color_error(self, device_qr, check_qr, mocker):
        """
        Test to check sending error with wrong length and device in database
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        qr = device_qr[0]
        scan_check_out_list = check_qr.scan_check_out_list(qr)
        for i in scan_check_out_list:
            message = i()
            if message:
                assert message[0] == f'Error: Wrong qr length {len(qr)}'

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_scan_check_out_list_with_correct_qr_and_db_none(self, device_qr, check_qr, mocker):
        """
        Test to check sending error with correct length and device not in database
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=None)
        qr = device_qr[0]
        scan_check_out_list = check_qr.scan_check_out_list(qr)
        for i in scan_check_out_list:
            message = i()
            if message:
                assert message[0] == f'Not in DB'

    @pytest.mark.negative
    @pytest.mark.parametrize('device_qr', wrong_qr_list)
    def test_scan_check_out_list_with_errors(self, device_qr, check_qr, mocker):
        """
        Test to check sending error with wrong length and device not in database
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=None)
        qr = device_qr[0]
        scan_check_out_list = check_qr.scan_check_out_list(qr)
        list_message = list(_()[0] for _ in scan_check_out_list)
        message_1 = list_message[0]
        message_2 = list_message[1]
        assert message_1 == f'Error: Wrong qr length {len(qr)}'
        assert message_2 == 'Not in DB'

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_check_scanned_device_can_add_device(self, device_qr, check_qr, mocker):
        """
        Test to check a message has been received about the ability to add a device. No errors.
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        mocker.patch('scanner_handler.CheckQr.can_add_device', return_value=True)
        qr = device_qr[0]
        check_qr.check_scanned_device(qr)
        assert check_qr.can_add_device.call_args[0][0] == f"hallelujah {qr}"

    @pytest.mark.negative
    @pytest.mark.parametrize('device_qr', wrong_qr_list)
    def test_check_scanned_device_can_add_device_wrong(self, device_qr, check_qr, mocker):
        """
        Test to check a message has been received about the ability to add a device. Wrong QR.
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=True)
        mocker.patch('scanner_handler.CheckQr.can_add_device', return_value=True)
        qr = device_qr[0]
        check_qr.check_scanned_device(qr)
        assert check_qr.can_add_device.call_args is None

    @pytest.mark.parametrize('device_qr', correct_qr_list)
    def test_check_scanned_device_can_add_device_wrong(self, device_qr, check_qr, mocker):
        """
        Test to check a message has been received about the ability to add a device. QR not in database.
        """
        mocker.patch('scanner_handler.CheckQr.check_in_db', return_value=None)
        mocker.patch('scanner_handler.CheckQr.can_add_device', return_value=True)
        qr = device_qr[0]
        check_qr.check_scanned_device(qr)
        assert check_qr.can_add_device.call_args is None



