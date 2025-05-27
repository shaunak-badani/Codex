import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import BackdropWithSpinner from "@/components/ui/backdropwithspinner";
import backendClient from "@/backendClient";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

import Markdown from 'react-markdown';

interface QuestionAnswer {
  id: number;
  question: string;
  answer: string;
}

const Mean = () => {

    const [isLoading, setLoading] = useState(false);
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState<QuestionAnswer>({id: 1, question: "", answer: ""});

    const presetValues = [
        "How do I write a static function in Java?",
        "How do I call an API in React?"
    ]

    const handlePromptInput = async(query: string) => {
        setLoading(true);
        const response = await backendClient.get("/prompt", {
            params: {
                query: query
            }
        });
        console.log(response);
        setResponse(response.data);
        setLoading(false);
    }

    return (
        <>
            <Textarea
                value={query}
                onChange = {(e) => setQuery(e.target.value)} 
                placeholder="Enter your coding-related query here!" />
            <div className="my-6">
                <Select onValueChange={setQuery}>
                    <SelectTrigger id="querySelector">
                    <SelectValue placeholder="Choose a sample query from the presets.." />
                    </SelectTrigger>
                    <SelectContent position="popper">
                    {presetValues.map((preset, index) => 
                        (<SelectItem
                            key={index}
                            value={preset} 
                            >
                            {preset}
                        </SelectItem>)
                    )}
                    </SelectContent>
                </Select>
            </div>
            <Button className="p-6 sm:p-6 rounded-2xl m-8 sm:m-8" onClick={() => handlePromptInput(query)}>
                Send
            </Button>
            {response.answer.length > 0 && <Markdown>{response.answer}</Markdown>}
            {isLoading && <BackdropWithSpinner />}
        </>
    )
};


export default Mean;