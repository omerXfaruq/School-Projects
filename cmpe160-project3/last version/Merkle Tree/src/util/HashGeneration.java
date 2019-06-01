/**
 * Taken from http://www.codejava.net/coding/how-to-calculate-md5-and-sha-hash-values-in-java
 */

package util;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class HashGeneration {
	public static String generateSHA256(String message) throws NoSuchAlgorithmException, UnsupportedEncodingException {
		return hashString(message, "SHA-256");
	}
	
	public static String generateSHA256(File file) throws NoSuchAlgorithmException, IOException {
	    return hashFile(file, "SHA-256");
	}

	private static String hashString(String message, String algorithm) throws NoSuchAlgorithmException, UnsupportedEncodingException {
		MessageDigest digest = MessageDigest.getInstance(algorithm);
		byte[] hashedBytes = digest.digest(message.getBytes("UTF-8"));
		return convertByteArrayToHexString(hashedBytes);
	}

	private static String convertByteArrayToHexString(byte[] arrayBytes) {
		StringBuffer stringBuffer = new StringBuffer();
		for (int i = 0; i < arrayBytes.length; i++) {
			stringBuffer.append(Integer.toString((arrayBytes[i] & 0xff) + 0x100, 16)
					.substring(1));
		}
		return stringBuffer.toString();
	}

	private static String hashFile(File file, String algorithm) throws NoSuchAlgorithmException, IOException {
		FileInputStream inputStream = new FileInputStream(file);
		MessageDigest digest = MessageDigest.getInstance(algorithm);

		byte[] bytesBuffer = new byte[1024];
		int bytesRead = -1;

		while ((bytesRead = inputStream.read(bytesBuffer)) != -1) {
			digest.update(bytesBuffer, 0, bytesRead);
		}
		inputStream.close();
		byte[] hashedBytes = digest.digest();
		return convertByteArrayToHexString(hashedBytes);
	}
}
