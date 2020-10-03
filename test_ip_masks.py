import pytest
from . import ip_masks
from .ip_masks import *


@pytest.mark.parametrize('ip, mask, expected', [
    ([192, 168, 1, 2], [255, 255, 255, 255], [192, 168, 1, 2]),
    ([192, 168, 1, 2], [255, 192, 0, 0], [192, 128, 0, 0]),
    ([192, 168, 1, 2], [255, 255, 255, 192], [192, 168, 1, 0])
])
def test_apply_mask(ip, mask, expected):

    assert apply_mask(ip, mask) == expected


@pytest.mark.parametrize('bit, expected', [
    (32, [255, 255, 255, 255]),
    (24, [255, 255, 255, 0]),
    (11, [255, 224, 0, 0]),
    (0, [0, 0, 0, 0])
])
def test_form_mask(bit, expected):

    assert form_mask(bit) == expected


@pytest.mark.parametrize('ip_list, apply_mask_result, expected', [
    ([1, 2, 3], [1, 1, 1], 1),
    ([1, 2, 3], [0, 1, 1], None),
    ([1, 2, 3], [1, 0, 1], None),
    ([], [1, 1, 1], None)
])
def test_check_mask(ip_list, apply_mask_result, expected, mocker):
    mocker.patch.object(ip_masks, 'apply_mask').side_effect = apply_mask_result

    assert check_mask(ip_list, []) == expected


@pytest.mark.parametrize('ip, expected', [
    (
        ['192.168.3.2', '192.168.1.2', '192.168.1.5'],
        [[192, 168, 3, 2], [192, 168, 1, 2], [192, 168, 1, 5]]
    ),
    (
        ['0.0.0.0'],
        [[0, 0, 0, 0]]
    ),
    (
        [], []
    )
])
def test_ip_str_to_list(ip, expected):

    assert ip_str_to_list(ip) == expected


@pytest.mark.parametrize('ip, exception', [
    (['192e.165.2.3'], ValueError),
    (['123.234.10.2.1'], IncorrectInputError),
    (['123.234.1'], IncorrectInputError),
    (['198.168.3.2', '198.256.87.0'], IncorrectInputError),
    (['198.168.-1.5'], IncorrectInputError)
])
def test_ip_str_to_list_with_exception(ip, exception):
    with pytest.raises(exception):
        ip_str_to_list(ip)


@pytest.mark.parametrize('result_mask', [
    [198, 168, 1, 0],
    [192, 168, 1, 2]
])
def test_find_mask(mocker, result_mask):
    mocker.patch.object(ip_masks, 'ip_str_to_list').return_value = mocker.Mock()
    mocker.patch.object(ip_masks, 'form_mask').return_value = mocker.Mock()
    mocker.patch.object(ip_masks, 'check_mask').return_value = result_mask

    assert find_mask(mocker.Mock()) == (32, result_mask)


def test_find_mask_with_error(mocker):
    mocker.patch.object(ip_masks, 'ip_str_to_list').return_value = mocker.Mock()
    mocker.patch.object(ip_masks, 'form_mask').return_value = mocker.Mock()
    mocker.patch.object(ip_masks, 'check_mask').return_value = None

    with pytest.raises(CanNotFindError):
        find_mask(mocker.Mock())
