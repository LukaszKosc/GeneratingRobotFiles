*** Settings ***
Documentation    Suite description

*** Keywords ***
I close
    [Arguments]    ${name_of_element}
    Log To Console    Bla bla

Opening keyword2
    When I open    slowo

I use
    [Arguments]    ${value}
    Log To Console    Saying sth stupid by ${value}

Check If this ${param} also works
    Log To Console    Another keyword with param: ${param}
