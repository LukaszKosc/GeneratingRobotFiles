*** Settings ***
Documentation    Suite description

*** Keywords ***
Show
    [Arguments]    ${name}
    Log To Console    It is menu2 showed by keyword

I open
    [Arguments]    ${what}
    Log to Console    Logging from "I open ${what}"

I need my second
    [Arguments]    ${what}
    Log to Console    Logging from "I open ${what}"

Verify If this keyword also works
    Log to Console    Logging from "Verify If this keyword also works"

Say If ${this} keyword ${also} works
    Log to Console    Logging from "Verify If this keyword also works"

