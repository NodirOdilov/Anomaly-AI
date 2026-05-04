import { DocH1, DocH2, DocLead, DocLi, DocOl, DocP } from '../components/DocTypography'

export function ReferencesPage() {
  return (
    <article className="pb-16">
      <DocH1>Литература и методические источники</DocH1>
      <DocLead>
        Перечень не исчерпывающий; приведены первичные работы и документация, релевантные используемым алгоритмам и
        оценочным процедурам. Оформление библиографических ссылок в публикациях — по стандарту целевого журнала (ГОСТ Р 7.0.5,
        APA, IEEE и т.д.).
      </DocLead>

      <DocH2 id="core-ml">Классическое машинное обучение</DocH2>
      <DocOl>
        <DocLi>
          Breiman L. Random Forests. <em>Machine Learning</em>, 2001, 45(1): 5–32. DOI: 10.1023/A:1010933404324.
        </DocLi>
        <DocLi>
          Friedman J., Hastie T., Tibshirani R. <em>The Elements of Statistical Learning</em>. Springer, 2nd ed., 2009.
        </DocLi>
        <DocLi>
          James G. et al. <em>An Introduction to Statistical Learning</em>. Springer, с изданиями с приложениями на R/Python.
        </DocLi>
      </DocOl>

      <DocH2 id="text">Текстовые признаки</DocH2>
      <DocOl>
        <DocLi>
          Manning C. D., Raghavan P., Schütze H. <em>Introduction to Information Retrieval</em>. Cambridge University Press,
          2008. (глава о векторизации и весах tf–idf).
        </DocLi>
      </DocOl>

      <DocH2 id="software">Программные реализации</DocH2>
      <DocP>
        Pedregosa F. et al. Scikit-learn: Machine Learning in Python. <em>Journal of Machine Learning Research</em>, 2011,
        12: 2825–2830. URL:{' '}
        <a className="text-cyan-300 underline-offset-2 hover:underline" href="https://jmlr.org/papers/v12/pedregosa11a.html">
          jmlr.org
        </a>
        .
      </DocP>
      <DocP>
        Документация scikit-learn по{' '}
        <span className="font-mono text-slate-200">TfidfVectorizer</span>,{' '}
        <span className="font-mono text-slate-200">LogisticRegression</span>,{' '}
        <span className="font-mono text-slate-200">RandomForestClassifier</span>,{' '}
        <span className="font-mono text-slate-200">Pipeline</span> — актуальная версия на{' '}
        <a className="text-cyan-300 underline-offset-2 hover:underline" href="https://scikit-learn.org/stable/">
          scikit-learn.org
        </a>
        .
      </DocP>

      <DocH2 id="security">Контекст кибербезопасности</DocH2>
      <DocP>
        Для постановки задач обнаружения вторжений и ограничений ML-смешения см. обзорные материалы NDSS, IEEE S&amp;P, USENIX
        Security по темам adversarial ML и operational security; конкретные ссылки рекомендуется подбирать под год
        публикации и юрисдикцию.
      </DocP>
    </article>
  )
}
