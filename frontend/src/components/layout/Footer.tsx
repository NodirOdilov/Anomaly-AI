export function Footer() {
  return (
    <footer className="border-t border-slate-800 px-6 py-4 text-sm leading-relaxed text-slate-400 lg:px-8">
      <p>Только защитное применение. Примеры payload предназначены для контрольной классификации на авторизованных данных.</p>
      <p className="mt-2">
        <a
          className="text-cyan-400/90 transition-colors hover:text-cyan-300 hover:underline"
          href="https://github.com/NodirOdilov/Anomaly-AI"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
        {' · '}
        <a
          className="text-cyan-400/90 transition-colors hover:text-cyan-300 hover:underline"
          href="https://github.com/NodirOdilov"
          target="_blank"
          rel="noopener noreferrer"
        >
          Nodir Odilov
        </a>
      </p>
    </footer>
  )
}
