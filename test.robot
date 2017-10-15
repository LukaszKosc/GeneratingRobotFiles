*** Settings ***
Resource    ./Keywords/Menu1/Menu1_Keywords.robot
Resource    ./Keywords/Menu2/Menu2_Keywords.robot
Documentation    Some weird stuff to include in one line :) - so far, only one line is supported.
*** Variables ***
${cokolwiek}  =    Set Variable    123
${param} =    Set Variable    123
${rowniez}  =    Set Variable    123
${that}  =    Set Variable    123

*** Test Cases ***
scenario1txt
    [Tags]    DEMO123 Tag1 tag2 tag3
    When I open  ${cokolwiek}
    Then I use     czegos
    Given I close     colowiek
    Then Verify If this keyword also works
    Then Check If this ${param}  also works
    Then Say If ${that} keyword ${rowniez}  works
    #some comment


jjjj

