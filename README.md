# University Website Selenium Testing with Jenkins

## 1. Project Overview
This project automates testing of the BITM university website using Selenium WebDriver and Java. Maven is used to manage dependencies and execute tests, while Jenkins integrates the test execution into a CI pipeline using code hosted on GitHub.

**Website:** https://www.bitm.edu.in/

## 2. Technologies Used
- Java
- Selenium WebDriver
- JUnit 5
- Maven
- Jenkins
- Git and GitHub
- Google Chrome

## 3. Test Cases
1. Verify the university website title.
2. Verify that links exist on the website.
3. Verify the visibility of navigation items.
4. Verify that visible links have destinations.
5. Verify that the Undergraduate submenu link exists.
6. Verify navigation to the Undergraduate Programs page.

## 4. Run Tests Locally
Ensure Java, Maven, and Google Chrome are installed.

Open a terminal in the project directory and run:

```bash
mvn clean test
```

## 5. Jenkins Integration
The Jenkins pipeline retrieves the source code from GitHub, runs the Maven test suite, and publishes the JUnit test reports.

**GitHub Repository:** https://github.com/Harshithat2005/university-selenium-testing

## 6. Test Results
The successful Jenkins build reported:

- Total tests: 6
- Passed: 6
- Failed: 0
- Skipped: 0

## 7. Expected Output
Jenkins displays the build status and test results, allowing the automated tests to be reviewed after each execution.
