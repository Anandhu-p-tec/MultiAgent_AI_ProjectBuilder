import { useState } from "react";
import api from "../api/client";

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function get(path: string) {
    try {
      setLoading(true);
      const res = await api.get(path);
      return res.data;
    } catch (e: any) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }

  async function post(path: string, body: any) {
    try {
      setLoading(true);
      const res = await api.post(path, body);
      return res.data;
    } catch (e: any) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }

  return { get, post, loading, error };
}
