# task-flask-user-api

endpoint_prefix = `/api/auth`

### Task endpoints

| Endpoints | Request Type | Details | 
|-----|-----|-----|
| `/task` | GET | Get all tasks of logged user. |
| `/task` | POST | Create a task. |
| `/task/{id}` | GET | Details of specific task. |
| `/task/{id}` | PUT | Update the specific task. |
| `/task/{id}` | DELETE | Delete the specfic task. |
| `/task/{task_id}/assign/{user_id}` | GET | Assign Task to given User. |


#### `/task` : GET

- Manager will get all the tasks.
- Team lead will get all the tasks they created.
- Employee will get task they are assigned either by Manager or Team Lead.

#### `/task` : POST

- Manager can create task.
- Team lead can create task.

#### `/task/{id}` : GET

- Manager can see details of any task.
- Team lead can see details of its tasks only.
- Employee can see details of assigned tasks.

#### `/task/{id}/update` : PUT

- Update the details of task.
- Task can only be updatd by manager and team lead.
- Employee can update the following status, 'started', 'in-progress', 'completed', of the task assigned only.

#### `/task/{id}/delete` : DELETE

- Task can only be deleted by Manager and Team lead.
- Manager can delete any task.

#### `/task/{id}/assign/{user_id}` : GET

- Assign the task id to the given user id.
- Manager can assign task to Team lead.
- Team lead can assign task to employee.