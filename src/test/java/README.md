
# University Website Selenium Testing

## Project Overview
Automated testing of the BITM university website using Selenium WebDriver and Java.

Website: https://www.bitm.edu.in/

## Technologies Used
- Java
- Selenium WebDriver
- JUnit 5
- Maven
- Git and GitHub
- Jenkins (CI/CD integration)

## Test Cases
1. Verify the website title.
2. Check that website links exist.
3. Verify navigation menu visibility.
4. Check visible links for destinations.
5. Verify the undergraduate program submenu.
6. Test navigation to the undergraduate programs page.

## Run Tests
Ensure Java, Maven, and Google Chrome are installed.

Run the following command from the project directory:

```bash
mvn clean test
```

## Test Reports
Maven Surefire generates JUnit XML reports in:

`target/surefire-reports/`
