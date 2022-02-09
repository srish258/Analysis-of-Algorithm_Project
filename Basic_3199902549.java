import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.lang.Math;
import java.util.*;

public class Basic_3199902549{
	static int gapPenalty = 30;
	public static void main(String[] args) {
		Runtime runtime = Runtime.getRuntime();
		long sm = runtime.totalMemory() - runtime.freeMemory();
		long st = System.currentTimeMillis();

		File input_file = new File(System.getProperty("user.dir") + "/" + args[0]);

		if(input_file.exists()){
			//#####################################################################################################
			File output = new File(System.getProperty("user.dir"), "output.txt");
			if(output.exists()){
				output.delete();
			}
			try{
				output.createNewFile();
			}
			catch(Exception e){
				e.printStackTrace();
			}
			//######################################################################################################

			//######################################################################################################
			ArrayList<Integer> str1_genratedIndices = new ArrayList<Integer>();
			ArrayList<Integer> str2_genratedIndices = new ArrayList<Integer>();
			String str1_base = null;
			String str2_base = null;

			boolean jDone = false;

			try{
				Scanner read = new Scanner(input_file);
				while(read.hasNextLine()){
					String line = read.nextLine();

					if(str1_base == null){
						str1_base = line;
					}
					else if((line.charAt(0) == 'A') ||
							(line.charAt(0) == 'C') ||
							(line.charAt(0) == 'G') ||
							(line.charAt(0) == 'T')){
						str2_base = line;
						jDone = true;
					}
					else{
						if(!jDone){
							str1_genratedIndices.add(Integer.parseInt(line));
						}
						else{
							str2_genratedIndices.add(Integer.parseInt(line));
						}
					}
				}

			}
			catch(FileNotFoundException e) {
				System.out.println("An error occurred while parsing the input.txt file.");
				e.printStackTrace();
			}
			//###################################################################################


			//###################################################################################

			String str1 = GS(str1_base, str1_genratedIndices);
			Integer predictedLengthX = (int)Math.pow(2, str1_genratedIndices.size()) * str1_base.length();
			if(str1.length() != predictedLengthX) {
				// TODO: Throw Error?
				System.out.println("Not same length");
			}

			// Parse second base string
			String str2 = GS(str2_base, str2_genratedIndices);
			Integer predictedLengthY = (int)Math.pow(2, str2_genratedIndices.size()) * str2_base.length();
			if(str2.length() != predictedLengthY) {
				// TODO: Throw Error?
				System.out.println("Not same length");
			}
			Map<String, String> result = SequenceAlignment_NWalgo(str1, str2);
			//#################################################################################
			// first 50, last 50
			//#################################################################################
			String X1_str1 = result.get("X_str1_result");
			String Y1_str2 = result.get("Y_str2_result");
			String X2_str1 = result.get("X_str1_result");
			String Y2_str2 = result.get("Y_str2_result");

			if (result.get("Y_str2_result").length() > 50){
				Y2_str2 = result.get("Y_str2_result").toString().substring(result.get("Y_str2_result").length()-50,result.get("Y_str2_result").length());
				Y1_str2 = result.get("Y_str2_result").toString().substring(0,50);

			}
			if (result.get("X_str1_result").length() > 50){
				X2_str1 = result.get("X_str1_result").toString().substring(result.get("X_str1_result").length()-50,result.get("X_str1_result").length());
				X1_str1 = result.get("X_str1_result").toString().substring(0,50);
			}

			String X_str1 = X1_str1 + " " + X2_str1;
			String Y_str2 = Y1_str2 + " " + Y2_str2;
			//##################################################################################
			// save to output (final strs and cost)
			//##################################################################################
			sendToOutput(X_str1, Y_str2);
			sendToOutput(result.get("Cost").toString(), "");


			//#################################################################################
			// time and memory used save to output
			//#################################################################################
			long et = System.currentTimeMillis();
			Double tt = (et - st)/1000.0;
			long em = runtime.totalMemory() - runtime.freeMemory();
			Double mt = (em - sm)/1024.0;
			sendToOutput(tt.toString(), "");
			sendToOutput(mt.toString(), "");
			//#################################################################################
		}
		else{
			System.out.println("input.txt file was not found.");
		}
	}
	//#########################################################################################
	// implement nw algo as per book
	//########################################################################################
	public static Map<String, String> SequenceAlignment_NWalgo(String str1, String str2) {

		int n = str1.length()+1;
		int m = str2.length()+1;
		int[][] dp = new int[m][n];



		//####################################################################################
		//Base case

		for (int j = 0; j < n; j++) {
			dp[0][j] = j * gapPenalty;
		}

		for (int i = 0; i < m; i++) {
			dp[i][0] = i * gapPenalty;
		}

		//recurrence relation
		// opt loop
		for (int i = 1; i < m; i++) {
			for (int j = 1; j < n; j++) {
				if(str2.charAt(i-1) == str1.charAt(j-1)) {
					dp[i][j] = dp[i-1][j-1];
				} else {
					dp[i][j] = Math.min(dp[i - 1][j - 1] + getMPmatrix(str2.charAt(i-1),str1.charAt(j-1)),
							Math.min(dp[i][j - 1] + gapPenalty, dp[i - 1][j] + gapPenalty));
				}
			}
		}
		//####################################################################################
		// DP --- iteratively
		String align_str1 = "";
		String align_str2 = "";
		int i = m-1; // X Columns
		int j = n-1; // Y Rows
		while((i > 0) || (j > 0)){
			if((i > 0) && (j > 0) && (str2.charAt(i-1) == str1.charAt(j-1))){
				align_str1 = align_str1 + String.valueOf(str1.charAt(j-1));
				align_str2 = align_str2 + String.valueOf(str2.charAt(i-1));
				j--;
				i--;
			}
			else if((j > 0) && (dp[i][j] == (dp[i][j - 1] + gapPenalty))){
				align_str1 = align_str1 + String.valueOf(str1.charAt(j-1));
				align_str2 = align_str2 + "_";
				j--;
			}
			else if((i > 0) && (j > 0) && (dp[i][j] == (dp[i - 1][j - 1] + getMPmatrix(str2.charAt(i-1),str1.charAt(j-1)))) ){
				align_str1 = align_str1 + String.valueOf(str1.charAt(j-1));
				align_str2 = align_str2 + String.valueOf(str2.charAt(i-1));
				j--;
				i--;

			}
			else if((i > 0) && (dp[i][j] == (dp[i-1][j] + gapPenalty))){
				align_str1 = align_str1 + "_";
				align_str2 = align_str2 + String.valueOf(str2.charAt(i-1));
				i--;
			}
		}
		StringBuffer reverse_align_str1 = new StringBuffer(align_str1);
		reverse_align_str1.reverse();
		StringBuffer reverse_align_str2 = new StringBuffer(align_str2);
		reverse_align_str2.reverse();

		align_str1 = reverse_align_str1.toString();
		align_str2 = reverse_align_str2.toString();
		Double minPenalty = Double.valueOf(dp[m-1][n-1]);
		String cost = (minPenalty).toString();
		Map<String, String> result = new HashMap<String, String>();
		result.put("X_str1_result", align_str1);
		result.put("Y_str2_result", align_str2);
		result.put("Cost", cost);
		return result;
		//###################################################################################
	}
	//#######################################################################################

	// Add data to the output.txt file
	//########################################################################################
	//save to output
	public static void sendToOutput(String line1, String line2) {
		try{
			FileWriter output = new FileWriter(System.getProperty("user.dir") + "/output.txt", true);

			BufferedWriter buffer = new BufferedWriter(output);

			if(line1!= null && !(line1 == "")){
				buffer.write(line1);
				buffer.newLine();
			}

			if(line2!= null && !(line2 == "")){
				buffer.write(line2);
				buffer.newLine();
			}
			buffer.close();
			output.close();
		}
		catch(Exception e){
			System.out.println("An error occurred while writing to the output.txt file.");
			e.printStackTrace();
		}
	}
	//#########################################################################################

	// mismatch penalty
	//########################################################################################
	// mismatch matrix stuff
	//########################################################################################
	public static int getMPmatrix(char x, char y) {
		int MP_matrix = 0;
		if (x == y) {
			return 0;
		} else if ((x == 'A' && y == 'T') || (x == 'T' && y == 'A')) {
			MP_matrix = 94;
		} else if ((x == 'C' && y == 'G') || (x == 'G' && y == 'C')) {
			MP_matrix = 118;
		} else if ((x == 'A' && y == 'C') || (x == 'C' && y == 'A') || (x == 'G' && y == 'T') || (x == 'T' && y == 'G'))  {
			MP_matrix = 110;
		} else if ((x == 'A' && y == 'G') || (x == 'G' && y == 'A') || (x == 'C' && y == 'T') || (x == 'T' && y == 'C')) {
			MP_matrix = 48;
		}
		return MP_matrix;
	}
	//#########################################################################################

	//#########################################################################################
	// srting generate function
	//#########################################################################################
	public static String GS(String str_base, ArrayList<Integer> str_genratedIndices){
		for (int i = 0; i < str_genratedIndices.size(); i++){
			String prev = str_base;
			str_base = prev.substring(0,str_genratedIndices.get(i)+1) + prev + prev.substring(str_genratedIndices.get(i)+1, prev.length());
		}
		return str_base;
	}
	//##########################################################################################


}