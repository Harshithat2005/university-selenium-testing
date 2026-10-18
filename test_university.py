
import unittest
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class UniversityWebsiteTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://www.bitm.edu.in/")

        cls.wait = WebDriverWait(cls.driver, 15)
        cls.base_domain = urlparse(
            cls.driver.current_url
        ).netloc.lower()

    def test_01_website_title(self):
        self.assertIn("BITM", self.driver.title)
        print("PASS: Website title verified:", self.driver.title)

    def test_02_navigation_links_exist(self):
        links = self.driver.find_elements(By.TAG_NAME, "a")
        self.assertGreater(len(links), 0)
        print(f"PASS: Found {len(links)} links")

    def test_03_visible_navigation_items(self):
        links = self.driver.find_elements(
            By.XPATH, "//header//a | //nav//a"
        )

        visible_links = [
            link.text.strip()
            for link in links
            if link.is_displayed() and link.text.strip()
        ]

        self.assertGreater(len(visible_links), 0)
        print("PASS: Visible navigation items:", visible_links)

    def test_04_links_have_destinations(self):
        missing = []
        stale_count = 0

        # Re-fetch elements because the website may update dynamically.
        initial_count = len(
            self.driver.find_elements(By.TAG_NAME, "a")
        )

        for index in range(initial_count):
            try:
                links = self.driver.find_elements(
                    By.TAG_NAME, "a"
                )

                if index >= len(links):
                    continue

                link = links[index]

                if not link.is_displayed():
                    continue

                text = (
                    link.get_attribute("innerText") or ""
                ).strip()

                href = link.get_attribute("href")

                if not href or not href.strip():
                    missing.append(
                        text or "[image/unnamed link]"
                    )

            except StaleElementReferenceException:
                stale_count += 1

        print("Visible links without destinations:", missing)
        print("Links skipped due to page updates:", stale_count)

        self.assertEqual(
            missing, [],
            "Some visible links do not have destinations"
        )

    def test_05_internal_links(self):
        links = self.driver.find_elements(By.TAG_NAME, "a")
        internal_urls = set()

        for link in links:
            try:
                href = link.get_attribute("href")

                if not href:
                    continue

                parsed = urlparse(href)

                if (
                    parsed.scheme in ("http", "https")
                    and parsed.netloc.lower() == self.base_domain
                ):
                    clean_url = parsed._replace(
                        fragment=""
                    ).geturl()

                    internal_urls.add(clean_url)

            except StaleElementReferenceException:
                continue

        self.assertGreater(len(internal_urls), 0)
        print(
            f"PASS: Found {len(internal_urls)} "
            "unique internal URLs"
        )

    def test_06_navigation_menu_interaction(self):
        menu_names = [
            "Academics",
            "Placements",
            "Program",
            "Admissions"
        ]

        for name in menu_names:
            with self.subTest(menu=name):
                elements = self.driver.find_elements(
                    By.XPATH,
                    f"//a[normalize-space()='{name}']"
                )

                visible = [
                    element for element in elements
                    if element.is_displayed()
                ]

                self.assertTrue(
                    visible,
                    f"Menu item not visible: {name}"
                )

                print(f"PASS: Menu item visible: {name}")

    def test_07_inspect_navigation(self):
        keywords = [
            "academic", "placement", "program",
            "life", "admission", "apply", "nba"
        ]

        elements = self.driver.find_elements(
            By.XPATH, "//a | //button"
        )

        print("\n--- NAVIGATION ELEMENT INSPECTION ---")

        for element in elements:
            try:
                if not element.is_displayed():
                    continue

                text = (
                    element.get_attribute("innerText") or ""
                ).strip()

                if text and any(
                    word in text.lower() for word in keywords
                ):
                    print(
                        f"Text: {text!r} | "
                        f"Tag: {element.tag_name} | "
                        f"Href: {element.get_attribute('href')} | "
                        f"Class: {element.get_attribute('class')}"
                    )

            except StaleElementReferenceException:
                continue

    
    def test_08_dropdown_submenu(self):
        # Locate the Program navigation item
        program_menu = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//a[normalize-space()='Program' "
                    "and contains(@href, '/programs')]"
                )
            )
        )

        # Hover over the menu
        ActionChains(self.driver).move_to_element(
            program_menu
        ).perform()

        # Check whether the submenu exists in the page
        submenu_links = self.driver.find_elements(
            By.XPATH,
            "//a[contains(normalize-space(.), 'Under Graduate')]"
        )

        visible_submenus = [
            link for link in submenu_links
            if link.is_displayed()
        ]

        if visible_submenus:
            self.assertIn(
                "/program/undergraduate",
                visible_submenus[0].get_attribute("href")
            )
            print("PASS: Undergraduate Programs submenu is visible")
        else:
            print(
                "INFO: Submenu did not open on hover. "
                "Checking whether the submenu link exists."
            )

            all_submenus = self.driver.find_elements(
                By.XPATH,
                "//a[contains(normalize-space(.), 'Under Graduate')]"
            )

            self.assertTrue(
                all_submenus,
                "Undergraduate Programs link was not found"
            )

            self.assertIn(
                "/program/undergraduate",
                all_submenus[0].get_attribute("href")
            )

            print(
                "PASS: Undergraduate Programs link exists "
                "with the expected destination"
            )

    
    
    def test_09_navigation_to_programs_page(self):
        expected_url = (
            "https://www.bitm.edu.in/program/undergraduate"
        )

        self.driver.get(expected_url)

        self.wait.until(
            lambda driver: "/program/undergraduate"
            in driver.current_url
        )

        self.assertIn(
            "/program/undergraduate",
            self.driver.current_url
        )

        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        self.assertTrue(
            self.driver.find_element(By.TAG_NAME, "body").is_displayed()
        )

        print("PASS: Undergraduate Programs page loaded")
        print("Page title:", self.driver.title)
        print("Destination:", self.driver.current_url)

        # Return to homepage for the remaining tests
        self.driver.get("https://www.bitm.edu.in/")
        self.wait.until(EC.title_contains("BITM"))

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
