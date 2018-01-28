//package com.amazonaws.cloudhsm.examples;

import java.io.IOException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.security.Security;

import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

import com.cavium.cfm2.CFM2Exception;
import com.cavium.cfm2.Util;
import com.cavium.key.CaviumAESKey;
import com.cavium.key.CaviumKey;
import com.cavium.provider.CaviumProvider;

public class SymmetricKeyGeneration {
// Generate a 256-bit AES symmetric key and save it in the HSM
    public static void main(String[] args) {
        //LoginLogoutExample.loginWithExplicitCredentials();
        LoginLogoutExample.loginWithEnvVariables();
        new SymmetricKeyGeneration().generateAESKey(256, true);
        LoginLogoutExample.logout();
    }

    public Key generateAESKey(int keySize, boolean isPersistent) {
        KeyGenerator keyGen;
        try {
            //CaviumProvider cp = new CaviumProvider();
            //keyGen = KeyGenerator.getInstance("AES",cp);
            Security.addProvider(new CaviumProvider());
            keyGen = KeyGenerator.getInstance("AES","Cavium");
            keyGen.init(keySize);
            SecretKey aesKey = keyGen.generateKey();
            System.out.println("Generated the AES key");
            if(aesKey instanceof CaviumAESKey) {
                System.out.println("Key is of type CaviumAESKey");
                CaviumAESKey ck = (CaviumAESKey) aesKey;
                //Save the key handle. You'll need it to encrypt/decrypt in the future.
                System.out.println("Key handle = " + ck.getHandle());
                //Get the key label. The SDK generates this label for the key.
                System.out.println("Key label = " + ck.getLabel());
                System.out.println("Is the key extractable? : " + ck.isExtractable());
                
                //By default, keys are not saved in the HSM. 
                System.out.println("Is the key persistent? : " + ck.isPersistent());
                // Save the key in the HSM, if requested
                if(isPersistent){
                    System.out.println("Make the key persistent:");
                    makeKeyPersistent(ck);
                }
                System.out.println("Is key persistent? : " + ck.isPersistent());
                
                //Verify key type and size
                System.out.println("Key algorithm : " + ck.getAlgorithm());
                System.out.println("Key size : " + ck.getSize());
            }
            // Return the key
            return aesKey;
        } catch (NoSuchAlgorithmException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        //} catch (NoSuchProviderException e) {
            // TODO Auto-generated catch block
        //    e.printStackTrace();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } 
        return null;
    }
    
    public static void makeKeyPersistent(Key key) {
        CaviumAESKey caviumAESKey = (CaviumAESKey) key;
        try {
            Util.persistKey(caviumAESKey);
            System.out.println("Added Key to HSM");
        } catch (CFM2Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
