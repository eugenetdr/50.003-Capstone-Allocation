package com.seleniumtest;

import java.awt.*;
import java.util.Random;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class escSeleniumTest {
    //test inputs
    //private static String[] testInps = {"123","selenium","testing","student","whasg"};
    //for student
    private static String studentUsername = "2020" + Integer.toString(new Random().nextInt(101)); //generates string from 2020001 to 2020100
    private static String studentPassword = "password";
    //for admin
    private static String adminLogin = "admin"; //both username and password
    private static final String[] adminPageButtons = {"viewRequirements","approve","edit","logout"};

    private static final int testTimes = 3;

    public static void main(String[] args) throws InterruptedException {


        //System.setProperty("webdriver.chrome.driver", "C:/Users/Fion/Desktop/Term 5/50.003 ESC/pset3/chromedriver.exe");
        System.setProperty("webdriver.chrome.driver", "/usr/bin/chromedriver");
        WebDriver driver = new ChromeDriver();

        driver.get("http://127.0.0.1:8000/");

//      In main page
        WebElement studentButton = driver.findElement(By.xpath("//input[@value='Student']"));
        WebElement adminButton = driver.findElement(By.xpath("//input[@value='Admin']"));
        Thread.sleep(3000);                         //waits for buttons to be visible/clickable

        adminButton.click();
        Thread.sleep(3000);                         //waits for buttons to be visible/clickable

        for (int i=0; i<testTimes; i++) {
            String testinp = new escSeleniumTest().generateInp(10,"small"); //type is "small" "big" or "digit"
            String testinp2 = new escSeleniumTest().generateInp(5,"digits");
            System.out.println("Trying... Username: "+testinp+ " Password: " + testinp2);
            new escSeleniumTest().login(driver,testinp,testinp2);
        }

        //new escSeleniumTest().login(driver,testInps[2],testInps[2]);

        new escSeleniumTest().login(driver,adminLogin,adminLogin); //actual login success

        new escSeleniumTest().adminPage(driver,0); // {0:viewRequirements, 1:edit, 2:approve, 3:logout};

        new escSeleniumTest().clickHome(driver);

        new escSeleniumTest().clickLogout(driver);

        driver.quit();

// Test invalid login inputs:
// Problem is that the invalid login is to another page,
// need to navigate.back & re initialise the WebElements (to a different name) in order to sendKeys again.

//        for (int i=0;i<testInps.length;i++) { //this doesnt work, need to rename the webelements.
//            WebElement username = driver.findElement(By.name("username"));
//            WebElement password = driver.findElement(By.name("password"));
//            WebElement login = driver.findElement(By.xpath("//input[@type='submit']"));
//            WebElement back = driver.findElement(By.xpath("//input[@type='button']"));
//
//            System.out.println(testInps[i]);
//            username.sendKeys(testInps[i]);
//            password.sendKeys(testInps[i]);
//            login.click();
//            Thread.sleep(1000);
//            driver.navigate().back();
//            Thread.sleep(3000);
//            username.clear();
//        }

    }

    public void login(WebDriver driver, String inputU, String inputP) throws InterruptedException  { //this works for both admin and student login

        WebElement username = driver.findElement(By.name("username"));
        WebElement password = driver.findElement(By.name("password"));
        WebElement login = driver.findElement(By.xpath("//input[@type='submit']"));
        WebElement back = driver.findElement(By.xpath("//input[@type='button']"));

        Thread.sleep(3000);
        username.sendKeys(inputU);
        password.sendKeys(inputP);
        login.click();
        Thread.sleep(3000);

        try {
            WebElement viewRequirements = driver.findElement(By.xpath("//input[@value='View Requirements']"));
        } catch (NoSuchElementException e) {    //if login fails, will go back to login page and clear previous input
            System.out.println("Login failed");
            driver.navigate().back();
            Thread.sleep(3000);
            WebElement username1 = driver.findElement(By.name("username"));
            username1.clear();
        }
    }

    public void adminPage(WebDriver driver, int buttonNum) throws InterruptedException {
        WebElement viewRequirements = driver.findElement(By.xpath("//input[@value='View Requirements']"));
        WebElement edit = driver.findElement(By.xpath("//input[@value='Edit']")); //The draggable elements need testing as well
        WebElement approve = driver.findElement(By.xpath("//input[@value='Approve']"));
        WebElement logout = driver.findElement(By.xpath("//input[@value='Logout']"));
        WebElement[] adminPageButtons = {viewRequirements,edit,approve,logout};

        adminPageButtons[buttonNum].click();
        Thread.sleep(3000);
    }

    public void clickHome(WebDriver driver) throws InterruptedException {
        WebElement home = driver.findElement(By.xpath("//input[@value='Home']"));
        home.click();
        Thread.sleep(3000);
    }

    public void clickLogout(WebDriver driver) throws InterruptedException {
        WebElement logout = driver.findElement(By.xpath("//input[@value='Logout']"));
        logout.click();
        Thread.sleep(3000);

    }

    public String generateInp(int length, String type) {
        Random rnd = new Random();
        int digit = rnd.nextInt(10);
        String output = "";

        if (type.equals("small")) {
            for (int i=0; i<length; i++) {
                char small = (char) (rnd.nextInt(26) + 'a');
                output = output + small;        //digit or small or big
            }
        }
        else if (type.equals("small")) {
            for (int i=0; i<length; i++) {
                char big = (char) (rnd.nextInt(26) + 'A');
                output = output + big;        //digit or small or big
            }
        }
        else if (type.equals("digits")) {
            for (int i=0; i<length; i++) {
                String dig = Integer.toString(new Random().nextInt(10));
                output = output + dig;        //digit or small or big
            }
        } else {
            System.out.println("No such type");

        }

        return(output);
    }
}



