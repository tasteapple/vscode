// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.7.0 < 0.9.0;

contract VoicePhishingReport {
    struct Report {
        string reporterName;
        string reportDate;
        string region;
        bool isVictim;
        string bank;
        string accountNumber;
        string phoneNumber;
        string reportContent;
    }

    Report[] public reports;
    
    event ReportSubmitted(
        uint indexed reportId,
        string reporterName,
        string reportDate,
        string region,
        bool isVictim,
        string bank,
        string accountNumber,
        string phoneNumber,
        string reportContent
    );

    function submitReport(
        string memory _reporterName,
        string memory _reportDate,
        string memory _region,
        bool _isVictim,
        string memory _bank,
        string memory _accountNumber,
        string memory _phoneNumber,
        string memory _reportContent
    ) public {
        reports.push(Report(_reporterName, _reportDate, _region, _isVictim, _bank, _accountNumber, _phoneNumber, _reportContent));
        uint reportId = reports.length - 1;
        emit ReportSubmitted(reportId, _reporterName, _reportDate, _region, _isVictim, _bank, _accountNumber, _phoneNumber, _reportContent);
    }

    function getReport(uint _reportId) public view returns (
        string memory reporterName,
        string memory reportDate,
        string memory region,
        bool isVictim,
        string memory bank,
        string memory accountNumber,
        string memory phoneNumber,
        string memory reportContent
    ) {
        require(_reportId < reports.length, "Invalid report ID");
        Report memory report = reports[_reportId];
        return (
            report.reporterName,
            report.reportDate,
            report.region,
            report.isVictim,
            report.bank,
            report.accountNumber,
            report.phoneNumber,
            report.reportContent
        );
    }

    function getTotalReports() public view returns (uint) {
        return reports.length;
    }

    function findReports(string memory _bank, string memory _accountNumber, string memory _phoneNumber) public view returns (uint[] memory) {
        uint[] memory matchingReports = new uint[](reports.length);
        uint count = 0;
        for (uint i = 0; i < reports.length; i++) {
            if (keccak256(abi.encodePacked(reports[i].bank)) == keccak256(abi.encodePacked(_bank)) &&
                keccak256(abi.encodePacked(reports[i].accountNumber)) == keccak256(abi.encodePacked(_accountNumber)) &&
                keccak256(abi.encodePacked(reports[i].phoneNumber)) == keccak256(abi.encodePacked(_phoneNumber))) {
                matchingReports[count] = i;
                count++;
            }
        }
        uint[] memory result = new uint[](count);
        for (uint i = 0; i < count; i++) {
            result[i] = matchingReports[i];
        }
        return result;
    }
}
