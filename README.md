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


#### `/task`

- Manager and Team lead will get all the tasks they created, and will also get tasks which are completed by employee, and are pending for review by task creator. 
- Employee will get task they are assigned either by Manager or Team Lead.

#### `/task/{id}`

- Get details of specific task.

#### `/task/{id}/update`

- Update the details of task.
- Task can only be updatd by manager and team lead.
- Employee can update the status of the task assigned only.

#### `/task/{id}/delete`

- Task can only be deleted by Manager and Team lead.

#### `/task/{id}/assign/{user_id}`

- Assign the task id to the given user id.
- Manager can assign task to Team lead.
- Team lead can assign task to employee.