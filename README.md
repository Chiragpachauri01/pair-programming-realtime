# pair-programming-realtime
Real-Time Pair Programming App

**Overview**
This project is a real-time pair programming demo built using FastAPI, WebSockets, and PostgreSQL.
Two users can join the same room and collaborate on code in real time. It also includes a simple
mocked autocomplete system. The frontend is intentionally minimal and uses plain HTML + JavaScript.

**Features**
- Create or join rooms using a Room ID
- Real-time code syncing through WebSockets
- Two browser windows stay in sync instantly
- Mock autocomplete suggestion (rule-based)
- Very simple frontend for easy testing

**Running with Docker**
docker-compose up --build
Open API documentation at http://localhost:8000/docs

**Running Without Docker**
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Make sure PostgreSQL is running at:
postgres://postgres:postgres@localhost:5432/pairprog

**How to Test**
1. Create a Room (Swagger or frontend "Create Room")
2. Open frontend/minimal-demo.html
3. Open it again in another browser window
4. Join same Room ID in both windows
5. Type to see real-time sync
6. Type "def ", wait 600ms, then press TAB for autocomplete

**Architecture Summary**
- FastAPI handles REST + WebSockets
- WebSockets broadcast updates to everyone in the room
- In-memory state keeps updates fast
- Room code is saved to PostgreSQL after all users disconnect
- Autocomplete is simple rule-based logic

**Future Improvements**
- Real AI autocomplete
- React UI with Monaco editor or CodeMirror
- Cursor presence indicators
- Improve conflict handling by grouping edits together, keeping track of update versions, and adding simple line-level locking.
- Deployment on Render/Railway

**Limitations**
- In-memory state resets on server restart
- No authentication
- Basic last-write-wins logic
- Minimal UI

**Conclusion**
A working example of real-time collaboration using FastAPI and WebSockets, complete with a small
mocked autocomplete system.