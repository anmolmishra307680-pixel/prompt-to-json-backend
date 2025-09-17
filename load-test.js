// load-test.js
import http from 'k6/http';
import { sleep } from 'k6';
export let options = { vus: 50, duration: '3m' };

export default function () {
  let url = __ENV.TARGET_URL || 'http://localhost:8000/generate';
  let payload = JSON.stringify({ prompt: 'Design a small concrete bridge for pedestrians' });
  let params = { headers: { 'Content-Type': 'application/json' } };
  http.post(url, payload, params);
  sleep(1);
}