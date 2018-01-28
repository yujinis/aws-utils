//package com.amazonaws.cloudhsm.examples.crypto.symmetric;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.Base64;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.GCMParameterSpec;
//import com.amazonaws.cloudhsm.examples.key.symmetric.SymmetricKeyGeneration;
//import com.amazonaws.cloudhsm.examples.operations.LoginLogoutExample;
import com.cavium.key.CaviumAESKey;

public class SymmetricEncryptDecryptExample {
    String plainText = "This is a sample plaintext message";
    
    String aad = "AAD data";
    String transformation = "AES/GCM/NoPadding";
    int ivSizeInBytes=12;
    int tagLengthInBytes = 16;

    /* * AEAD modes, such as GCM and CCM, authenticate the AAD before authenticating the ciphertext. 
     * * To avoid buffering the ciphertext internally, supply all AAD data to GCM/CCM implementations
     * * before the ciphertext is processed.
     * */
    public static void main(String[] args) {

        SymmetricEncryptDecryptExample obj = new SymmetricEncryptDecryptExample();
        // LoginLogoutExample.loginWithExplicitCredentials();
        LoginLogoutExample.loginWithEnvVariables();

        // Generate an 256-bit AES key and save it in the HSM
        Key key =new SymmetricKeyGeneration().generateAESKey(256, true);

        // Generate an initialization vector (IV)
        byte[] iv = obj.generateIV(obj.ivSizeInBytes);
        System.out.println("Performing AES encryption operation");

        // Encrypt the plaintext with the specified algorithm, key, IV, and the AAD
        byte[] result = obj.encrypt(obj.transformation, (CaviumAESKey) key, obj.plainText, iv, obj.aad, obj.tagLengthInBytes);
        System.out.println("Plaintext is encrypted");
        System.out.println("Base64-encoded encrypted text = " + Base64.getEncoder().encodeToString(result));
        System.out.println("Decrypting the ciphertext");

        //Extract the IV for the decrypt operation
        iv = Arrays.copyOfRange(result, 0, 16);
        byte[] cipherText = Arrays.copyOfRange(result, 16, result.length);

        // Decrypt the ciphertext using the algorithm, key, IV, and AAD
        byte[] decryptedText = obj.decrypt(obj.transformation, (CaviumAESKey) key, cipherText, iv, obj.aad, obj.tagLengthInBytes);
        System.out.println("Plaintext = "+new String(decryptedText));
        LoginLogoutExample.logout();
    }

    // This encrypt operation uses an initialization vector (IV) and additional authenticated data (AAD)
    public byte[] encrypt(String transformation, CaviumAESKey key, String plainText, byte[] iv, String aad, int tagLength) {
        try {
            // Create an encryption cipher
            Cipher encCipher = Cipher.getInstance(transformation, "Cavium");
            // Create a parameter spec
            GCMParameterSpec gcmSpec = new GCMParameterSpec(tagLengthInBytes * 8, iv);
            // Configure the encryption cipher
            encCipher.init(Cipher.ENCRYPT_MODE, key, gcmSpec);
            encCipher.updateAAD(aad.getBytes());
            encCipher.update(plainText.getBytes());
            // Encrypt the plaintext data
            byte[] ciphertext = encCipher.doFinal();
            
            //Save the new IV and AADTag from the HSM.
            //You'll need them to create the GCMParameterSpec for the decrypt operation.
            byte[] finalResult = new byte[encCipher.getIV().length + ciphertext.length];
            System.arraycopy(encCipher.getIV(), 0, finalResult, 0,
            encCipher.getIV().length);
            System.arraycopy(ciphertext, 0, finalResult, encCipher.getIV().length,
            ciphertext.length);
            return finalResult;
        } catch (NoSuchAlgorithmException | NoSuchProviderException | NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (BadPaddingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }

    // Generate an initialization vector (IV)
    public byte[] generateIV(int ivSizeinByets) {
        SecureRandom sr;
        try {
            sr = SecureRandom.getInstance("AES-CTR-DRBG", "Cavium");
            byte[] iv = new byte[ivSizeinByets];
            sr.nextBytes(iv);
            return iv;
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }

    //Decrypt with the specified algorithm, key, ciphertext, IV, and AAD.
    public byte[] decrypt(String transformation, CaviumAESKey key, byte[] cipherText, byte[] iv, String aad, int tagLength) {
        Cipher decCipher;
        try {
            //Create the decryption cipher
            decCipher = Cipher.getInstance(transformation, "Cavium");

            // Create a Cavium parameter spec from the IV and AAD
            GCMParameterSpec gcmSpec = new GCMParameterSpec(tagLengthInBytes * 8,iv);

            //Configure the decryption cipher
            decCipher.init(Cipher.DECRYPT_MODE, key, gcmSpec);
            decCipher.updateAAD(aad.getBytes());

            //Decrypt the ciphertext and return the plaintext
            return decCipher.doFinal(cipherText);

        } catch (NoSuchAlgorithmException | NoSuchProviderException |
            NoSuchPaddingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (BadPaddingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }
}
