from typing import List, Tuple
import sys


def apply_mask(ip: list, mask: list) -> List:
    """
    Apply mask on IP.
    :param ip: a list of octets in IP
    :param mask: a list of octets in mask
    :return: a list of octets after applying mask on IP
    """

    return [el1 & el2 for el1, el2 in zip(ip, mask)]


def form_mask(bit: int, max_bit=32) -> List:
    """
    Create a bit form of the mask (e.g. 29 -> [255.255.255.248]
    :param bit: integer number of bits in mask
    :param max_bit: optional value, added for the future reference
    :return: a list of the octets in mask
    """

    step = max_bit // 4
    mask = []
    for el in range(step, max_bit + 1, step):
        if el <= bit:
            mask.append(255)
        else:
            raw_mask = '1' * (bit - (el - step)) + '0' * (el - bit)
            mask.append(int(raw_mask, 2))

    return mask


def check_mask(ip_list: list, mask: list) -> (None, List):
    """
    Function apply mask on the list of IPs and checks if the mask is correct.
    :param ip_list: the list of IPs (e.g. [[192, 168, 3, 2], [192, 168, 1, 2]])
    :param mask: the list of octets in mask
    :return: None if IP networks different, a list of ip network octets
    """

    def all_the_same(elements: list) -> bool:
        return elements[1:] == elements[:-1]

    if not ip_list:
        return

    network = []
    for ip in ip_list:
        network.append(apply_mask(ip, mask))
        if not all_the_same(network):
            return
    return network[0]


def ip_str_to_list(str_ip_list: list) -> List:
    """
    Check if IPs are valid and returns the list of IPs.
    -> ['192.168.3.2', '192.168.1.2', '192.168.1.5'],
    <- [[192, 168, 3, 2], [192, 168, 1, 2], [192, 168, 1, 5]]
    :param str_ip_list: a list of raw IPs
    :raise: IncorrectInputError in case of IPs are invalid
    :return: a list of IPs in correct form
    """
    try:
        ip_list = [list(map(int, ip.split('.'))) for ip in str_ip_list]
    except ValueError:
        print('Invalid IP - contains non integer values.')
        raise
    for ip in ip_list:
        if len(ip) != 4:
            raise IncorrectInputError(f"Invalid IP: {'.'.join(str(item) for item in ip)}. Incorrect parts!")
        if list(filter(lambda x: x < 0 or x > 255, ip)):
            raise IncorrectInputError(f"Invalid IP: {'.'.join(str(item) for item in ip)}. Incorrect values!")

    return ip_list


def find_mask(raw_ip_list: list) -> Tuple:
    """
    Move from 32 bit mask to 0 bit mask to find appropriate one.
    :param raw_ip_list: the list of IPs as a strings
    :raises: CanNotFindError in case of no mask is found
    :return: a tuple of number of subnet mask bits and the ip network
    """
    ip_list = ip_str_to_list(raw_ip_list)
    for subnet_mask in range(32, 0, -1):
        result_mask = check_mask(ip_list, form_mask(subnet_mask))
        if result_mask:
            return subnet_mask, result_mask

    raise CanNotFindError('Can not find appropriate mask!')


class CanNotFindError(Exception):
    def __init__(self, error_message: str):
        self.message = error_message


class IncorrectInputError(Exception):
    def __init__(self, error_message: str):
        self.message = error_message


if __name__ == '__main__':
    # check if we have only two args (only one arg is specified)
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            file_ip_list = f.readlines()
        s_mask, r_mask = find_mask(file_ip_list)
        print(f"Result net: {'.'.join(str(item) for item in r_mask)}/{s_mask}")
    else:
        print('Incorrect amount of parameters. Name of the file is required!')
        sys.exit(1)
