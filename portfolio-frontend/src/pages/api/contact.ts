/**
 * Endpoint del formulario de contacto (RF-23 a RF-26).
 *
 * Static-first: la clave de Web3Forms vive solo en el entorno del servidor.
 * Si algún día se pasa a `output: 'server'`, hay que.disabled CSRF porque
 * un endpoint público sin origen validado es abusable desde cualquier web.
 */

export const prerender = false;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const FIELDS = ['name', 'email', 'subject', 'message'] as const;

type Field = (typeof FIELDS)[number];

interface Payload {
  name?: string;
  email?: string;
  subject?: string;
  message?: string;
  /** Honeypot: si viene relleno, es un bot. */
  website?: string;
}

function json(status: number, body: Record<string, unknown>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function POST({ request }: { request: Request }): Promise<Response> {
  const apiKey = import.meta.env.WEB3FORMS_KEY;
  if (!apiKey) {
    console.error('[contact] WEB3FORMS_KEY no está definida');
    return json(500, { success: false, errors: ['server'] });
  }

  let payload: Payload;
  try {
    payload = await request.json();
  } catch {
    return json(400, { success: false, errors: ['body'] });
  }

  // Honeypot: se responde 200 para no dar pistas al bot.
  if (payload.website) {
    return json(200, { success: true });
  }

  // Misma validación que el cliente: los cuatro campos a la vez (RF-24/RF-25).
  const errors: Partial<Record<Field, string>> = {};
  for (const field of FIELDS) {
    const value = typeof payload[field] === 'string' ? payload[field].trim() : '';
    if (!value) {
      errors[field] = 'required';
    } else if (field === 'email' && !EMAIL_RE.test(value)) {
      errors[field] = 'invalid_email';
    }
  }

  if (Object.keys(errors).length > 0) {
    return json(400, { success: false, errors });
  }

  const accessKey = apiKey;

  try {
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        access_key: accessKey,
        name: payload.name!.trim(),
        email: payload.email!.trim(),
        subject: payload.subject!.trim(),
        message: payload.message!.trim(),
        from_name: 'Portfolio Web',
      }),
    });

    const result = (await response.json().catch(() => ({}))) as { success?: boolean };

    if (!response.ok || result.success === false) {
      console.error('[contact] Web3Forms respondió', response.status, result);
      return json(502, { success: false, errors: ['provider'] });
    }

    return json(200, { success: true });
  } catch (error) {
    console.error('[contact] fallo hablando con Web3Forms', error);
    return json(502, { success: false, errors: ['provider'] });
  }
}

export async function GET(): Promise<Response> {
  return json(405, { success: false, errors: ['method'] });
}