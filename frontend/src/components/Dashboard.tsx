import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Dashboard() {
  const [tasks, setTasks] = useState<any[]>([]);

  useEffect(() => {
    api.get("/tasks").then((res) => setTasks(res.data || []));
  }, []);

  return (
    <div>
      <h2 className="text-lg font-bold mb-4">Project Tasks</h2>
      <ul className="space-y-2">
        {tasks.map((task, idx) => (
          <li key={idx} className="bg-gray-100 p-2 rounded">
            {task.title} — <span className="text-sm">{task.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
