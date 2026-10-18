import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class UniversityWebsiteTests {

    static WebDriver driver;
    static WebDriverWait wait;

    @BeforeAll
    static void setUp() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        driver.get("https://www.bitm.edu.in/");
    }

    @Test
    void test01WebsiteTitle() {
        assertTrue(driver.getTitle().contains("BITM"));
        System.out.println("PASS: Website title verified");
    }

    @Test
    void test02LinksExist() {
        List<WebElement> links = driver.findElements(By.tagName("a"));
        assertTrue(links.size() > 0);
        System.out.println("PASS: Links found: " + links.size());
    }

    @Test
    void test03NavigationItemsVisible() {
        String[] menuNames = {
            "Academics", "Placements", "Programs", "Admissions"
        };

        for (String name : menuNames) {
            List<WebElement> menus = driver.findElements(
                By.xpath("//a[contains(normalize-space(.), '" + name + "')]")
            );

            boolean visible = false;

            for (WebElement menu : menus) {
                if (menu.isDisplayed()) {
                    visible = true;
                    break;
                }
            }

            assertTrue(visible, "Navigation item not visible: " + name);
            System.out.println("PASS: Navigation item visible: " + name);
        }
    }

    @Test
    void test04LinksHaveDestinations() {
        List<WebElement> links = driver.findElements(By.tagName("a"));
        int missing = 0;

        for (WebElement link : links) {
            String href = link.getAttribute("href");

            if (link.isDisplayed() && (href == null || href.isBlank())) {
                missing++;
            }
        }

        assertEquals(0, missing,
            "Visible links without destinations: " + missing);

        System.out.println("PASS: Visible links have destinations");
    }

    @Test
    void test05ProgramSubmenuExists() {
        WebElement submenu = wait.until(
            ExpectedConditions.presenceOfElementLocated(
                By.xpath("//a[contains(normalize-space(.), 'Under Graduate') " +
                    "and contains(@href, '/program/undergraduate')]")
            )
        );

        assertTrue(submenu.getAttribute("href")
            .contains("/program/undergraduate"));

        System.out.println("PASS: Undergraduate submenu link exists");
    }

    @Test
    void test06NavigateToProgramsPage() {
        driver.get("https://www.bitm.edu.in/program/undergraduate");

        wait.until(ExpectedConditions.urlContains("/program/undergraduate"));

        assertTrue(driver.getCurrentUrl().contains("/program/undergraduate"));
        assertTrue(driver.findElement(By.tagName("body")).isDisplayed());

        System.out.println("PASS: Undergraduate Programs page loaded");

        driver.get("https://www.bitm.edu.in/");
        wait.until(ExpectedConditions.titleContains("BITM"));
    }

    @AfterAll
    static void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
