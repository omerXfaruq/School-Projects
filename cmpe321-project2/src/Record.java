import java.util.StringTokenizer;

public class Record implements Comparable<Record> {
    public int primaryField;
    public String record;

    public Record(String record) {
        this.record = record;
        StringTokenizer tokenize = new StringTokenizer(record);
        primaryField = Integer.parseInt(tokenize.nextToken());
    }

    public String toString() {
        return record;
    }

    public int compareTo(Record d) {
        return Integer.valueOf(primaryField).compareTo(d.primaryField);
    }
}
