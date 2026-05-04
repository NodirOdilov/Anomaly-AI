import { Bento } from '../components/Bento'
import { CTA } from '../components/CTA'
import { DocsSection } from '../components/DocsSection'
import { Footer } from '../components/Footer'
import { Hero } from '../components/Hero'
import { HowItWorks } from '../components/HowItWorks'
import { LayoutBg } from '../components/LayoutBg'
import { MetricsStrip } from '../components/MetricsStrip'
import { Modules } from '../components/Modules'
import { Nav } from '../components/Nav'
import { Trust } from '../components/Trust'

export default function LandingPage() {
  return (
    <>
      <LayoutBg />
      <Nav variant="landing" />
      <main>
        <Hero />
        <MetricsStrip />
        <Bento />
        <Modules />
        <HowItWorks />
        <Trust />
        <DocsSection />
        <CTA />
      </main>
      <Footer />
    </>
  )
}
