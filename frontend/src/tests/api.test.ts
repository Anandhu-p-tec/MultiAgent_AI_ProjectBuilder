import { describe, it, expect } from "vitest";
import { api } from "../api/client";

describe("API Client", () => {
  it("has baseURL configured", () => {
    expect(api.defaults.baseURL).toContain("localhost");
  });
});
