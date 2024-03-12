//assignment 6th 8
import java.util.*;
class Student{
	int rno;
	String name;
	float per;
	static int count=0;
	Student(){
		rno=0;
		name=" ";
		per=0.0f;
	}
	Student(int rno,String name,float per){
		Scanner sc=sc.Scanner(System.in);
		
	}
	void count(){
		count++;
		System.out.println("Object is created"+count);

	}
	public String toString(){
		System.out.println("Roll no of student:-"+rno);
		System.out.println("Name of student:-"+name);
		System.out.println("Percentage of student"+per);
	}
	public static void main(String arg[]){
		Student st=new Student();
		Student st1=new Student(102,"sam",77.9f);
		st.Student();st1.Student();
		st.display(); st.count();
		st1.display(); st1.count();
    }
}