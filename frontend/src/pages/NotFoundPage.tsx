import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'

export function NotFoundPage() {
  return (
    <Card className="p-10 text-center">
      <div className="text-xl font-semibold text-slate-50">Страница не найдена</div>
      <p className="mt-3 text-sm leading-relaxed text-slate-300">Такой маршрут отсутствует в этой панели.</p>
      <div className="mt-4 flex justify-center">
        <Link to="/">
          <Button type="button">Вернуться на панель</Button>
        </Link>
      </div>
    </Card>
  )
}
