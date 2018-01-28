//package com.amazonaws.cloudhsm.examples;

import com.cavium.cfm2.CFM2Exception;
import com.cavium.cfm2.LoginManager;

public class LoginLogoutExample {
    public static void main(String[] args) {

/*
        System.out.println("Test three methods of logging into the HSMs in your cluster");
        System.out.println("*********** Logging in using hard-coded credentials ***********");
        loginWithExplicitCredentials();
        System.out.println("Logging out");
        logout();
        
        System.out.println("*********** Logging in using Java system properties ***********");    
        loginUsingJavaProperties();
        System.out.println("Logging out");
        logout();
*/
        
        System.out.println("*********** Logging in using environment variables ************");    
        loginWithEnvVariables();
        System.out.println("Logging out");
        logout();
    }

/**
 * Method #1: Use hard-coded credentials
 *
 * Replace "CryptoUser" and "CUPassword123!" with a valid user name and password.
 */
    public static void loginWithExplicitCredentials() {
        LoginManager lm = LoginManager.getInstance();
        lm.loadNative();
        try {
            lm.login("PARTITION_1", "CryptoUser", "CUPassword123!");
            int appID = lm.getAppid();
            System.out.println("App ID = " + appID);
            int sessionID = lm.getSessionid();
            System.out.println("Session ID = " + sessionID);
        } catch (CFM2Exception e) {
            e.printStackTrace();
        }
    }

/**
 * Method #2: Use Java system properties
 *
 * Replace "CryptoUser" and "CUPassword123!" with a valid user name and password.
 */
    public static void loginUsingJavaProperties() {
        System.setProperty("HSM_PARTITION","PARTITION_1"); 
        System.setProperty("HSM_USER","CryptoUser"); 
        System.setProperty("HSM_PASSWORD","CUPassword123!");
        LoginManager lm = LoginManager.getInstance();
        lm.loadNative();
        try {
            lm.login();
            int appID = lm.getAppid();
            System.out.println("App ID = " + appID);
            int sessionID = lm.getSessionid();
            System.out.println("Session ID = " + sessionID);
        } catch (CFM2Exception e) {
            e.printStackTrace();
        }
    }
    
/**
 * Method #3: Use environment variables
 *
 * Before invoking the JVM, set the following environment variables
 * using a valid user name and password
 *    export HSM_PARTITION=PARTITION_1
 *    export HSM_USER=<hsm-user-name>
 *    export HSM_PASSWORD=<password>
 */
    public static void loginWithEnvVariables() {
        LoginManager lm = LoginManager.getInstance();
        lm.loadNative();
        try {
            lm.login();
            int appID = lm.getAppid();
            System.out.println("App ID = " + appID);
            int sessionID = lm.getSessionid();
            System.out.println("Session ID = " + sessionID);
        } catch (CFM2Exception e) {
            e.printStackTrace();
        }
    }
    
    public static void logout() {
        try {
            LoginManager.getInstance().logout();
        } catch (CFM2Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
