import Mean from '../model-cards/mean'
import { Card } from "@/components/ui/card"



function Home() {
    return (
        <div>
              <h1 className="scroll-m-20 tracking-tight lg:text-3xl">
                A coding assistant at your fingertips!
              </h1>
              <p className="leading-7 [&:not(:first-child)]:mt-6 m-6 sm:m-6">
                Codex allows you to ask any coding-related questions to a state-of-the-art Qwen 2.5 Coder 7B model, without incurring large costs to call an LLM like ChatGPT, Gemini,
                or Claude.
              </p>
              <Card className="p-20">
                <Mean />
              </Card>
            </div>
    );
  }
  
  export default Home;