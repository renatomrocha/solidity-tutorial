// SPDX-License-identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 private number;

    struct People {
        string name;
        uint256 age;
    }

    // Dynamic size array
    People[] public people;

    mapping(string => People) public peopleMap;

    function addPerson(string memory _name, uint256 _age) public {
        peopleMap[_name] = People(_name, _age);
    }

    function store(uint256 _number) public returns(uint256){
        number = _number;
        return number;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }
}
