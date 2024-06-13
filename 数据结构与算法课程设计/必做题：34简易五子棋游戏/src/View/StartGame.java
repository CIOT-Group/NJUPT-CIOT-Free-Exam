/***
 *               _                           _
 *    __ _  ___ | |__   __ _ _ __   __ _    (_) __ ___   ____ _
 *   / _` |/ _ \| '_ \ / _` | '_ \ / _` |   | |/ _` \ \ / / _` |
 *  | (_| | (_) | |_) | (_| | | | | (_| |   | | (_| |\ V | (_| |
 *   \__, |\___/|_.__/ \__,_|_| |_|\__, |  _/ |\__,_| \_/ \__,_|
 *   |___/                         |___/  |__/
 */

package View;

public class StartGame {

    public static void main(String[] args) {
        System.out.println("               _                           _");
        System.out.println("    __ _  ___ | |__   __ _ _ __   __ _    (_) __ ___   ____ _");
        System.out.println("   / _` |/ _ \\| '_ \\ / _` | '_ \\ / _` |   | |/ _` \\ \\ / / _` |");
        System.out.println("  | (_| | (_) | |_) | (_| | | | | (_| |   | | (_| |\\ V | (_| |");
        System.out.println("   \\__, |\\___/|_.__/ \\__,_|_| |_|\\__, |  _/ |\\__,_| \\_/ \\__,_|");
        System.out.println("   |___/                         |___/  |__/\n");

        System.out.println("################### Gobang Java Project ###################");

        new PCMainBoard();
    }
}