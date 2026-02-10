```md
# Task-Pilot-DB

PostgreSQL Data Service for Task-Pilot

This service owns **ALL persistent data**.

---

## 🧩 Responsibilities

• Users  
• Tasks  
• Subtasks  
• AI history  
• Authentication data  

It exposes a **pure REST API** for all data access.

---

## 🗃 Database Tables

### users
| Column | Type |
|-------|------|
| id | int |
| email | string |
| password | hashed |
| name | string |

---

### tasks
| Column | Type |
|--------|------|
| id | int |
| user_id | int |
| task | string |
| description | string |
| priority | string |
| date | date |
| done | boolean |

---

### subtasks
| Column | Type |
|--------|------|
| id | int |
| task_id | int |
| title | string |
| estimate | string |
| priority | string |
| completed | boolean |
| source | ai/manual |

---

### ai_history
| Column | Type |
|--------|------|
| id | int |
| user_id | int |
| prompt | string |
| response | json |
| type | string |
| summary | string |

---

## 🔐 Security

This service does **NOT** do auth.

The UI Backend sends validated user IDs.

---

## 🚀 Run locally

```bash
uvicorn main:app --port 5014
