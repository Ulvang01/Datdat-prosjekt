import os

from src.python.models import EmployeeStatus, Contributor, Task, TaskContributorJunction, Play

employeeStatusPath = os.path.join("src", "res", "employeestatus.txt")
contributorsPath = os.path.join("src", "res", "contributors.txt")

def verifyStatus(cursor):
    """ Verify EmployeeStatus in database"""
    try:
        cursor.execute("BEGIN;")
        with open(employeeStatusPath, 'r') as file:
            print("Reading contributors...")
            content = file.readlines()
        
        employee_status_list = []
        for i in range(len(content)):
            employee_status_list.append(EmployeeStatus(content[i].strip()))
        
        EmployeeStatus.upsert_batch(cursor, employee_status_list)
        cursor.execute("COMMIT;")
        print("Done verifying employee statuses...")

    except Exception as e:
        print("Error verifying employee status...")
        print(e.with_traceback(e.__traceback__))
        cursor.execute("ROLLBACK;")
        return
    
def verifyContributors(cursor):
    """ Verify Contributors in database"""
    try:
        cursor.execute("BEGIN;")
        with open(contributorsPath, 'r') as file:
            print("Reading contributors...")
            content = file.readlines()
        
        content = [x.split(":") for x in content]
        
        for i in range(len(content)):
            print("Verifying contributors...")
            contributors = Contributor(None, content[i][0].strip(), "null", EmployeeStatus.get_by_status(cursor, "employee"))
            contributors.insert(cursor)
            contributors = Contributor.get_by_name(cursor, contributors.name)
            tasks = content[i][1].split("/")
            for t in tasks:
                print(content[i][2].strip())
                task = Task.get_by_name_and_play(cursor, t.strip(), Play.get_by_name(cursor, content[i][2].strip()))
                if task is None or task.id is None:
                    task = Task(None, t.strip(), Play.get_by_name(cursor, content[i][2].strip()))
                    task.insert(cursor)
                    task = Task.get_by_name_and_play(cursor, task.name, task.play)
                junction = TaskContributorJunction(contributors, task)
                junction.insert(cursor)

        cursor.execute("COMMIT;")
        print("Done verifying contributors...")
    except Exception as e:
        print("Error verifying contributors...")
        print(e.with_traceback(e.__traceback__))
        cursor.execute("ROLLBACK;")
        return

def verifyContributorsAndStatus(conn):
    cursor = conn.cursor()
    verifyStatus(cursor)
    verifyContributors(cursor)
    conn.commit()