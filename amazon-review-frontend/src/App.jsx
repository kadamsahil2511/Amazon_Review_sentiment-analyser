import { useState } from 'react'
import { Textarea } from './components/ui/textarea'
import { Button } from './components/ui/button'
import { Loader2, MessageSquare, ShieldAlert, Sparkles, AlertCircle } from 'lucide-react'

function App() {
  const [review, setReview] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeSentiment = async () => {
    if (!review.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('https://sahilskadam-amazon-sentiment-api.hf.space/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: review })
      });

      if (!response.ok) throw new Error('API Request Failed');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze sentiment.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-50 py-12 px-4 selection:bg-neutral-200 dark:selection:bg-neutral-800">
      <div className="max-w-2xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="text-center space-y-3">
          <div className="inline-flex justify-center items-center h-12 w-12 rounded-full bg-neutral-900 dark:bg-white text-white dark:text-neutral-900 mb-2 shadow-sm">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Amazon Review Analyzer</h1>
          <p className="text-neutral-500 dark:text-neutral-400">
            Powered by Logistic Regression & TF-IDF
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl shadow-sm p-6 space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              Paste a product review below:
            </label>
            <Textarea 
              placeholder="e.g. This product is absolutely fantastic! Highly recommended."
              className="resize-none h-32 text-base"
              value={review}
              onChange={(e) => setReview(e.target.value)}
              disabled={loading}
            />
          </div>
          
          <Button 
            className="w-full text-base h-11 transition-all"
            onClick={analyzeSentiment}
            disabled={!review.trim() || loading}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : "Analyze Sentiment"}
          </Button>
        </div>

        {/* Error State */}
        {error && (
          <div className="animate-in fade-in slide-in-from-bottom-2 bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 p-4 rounded-xl border border-red-100 dark:border-red-900/50 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="animate-in fade-in zoom-in-95 duration-200 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-8 text-center space-y-4 shadow-sm">
            
            <div className="space-y-1">
              <p className="text-sm font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-widest">
                Prediction
              </p>
              <h2 className={`text-4xl font-extrabold tracking-tight ${
                result.sentiment === 'Positive' 
                  ? 'text-neutral-900 dark:text-white' 
                  : 'text-neutral-500 dark:text-neutral-400'
              }`}>
                {result.sentiment}
              </h2>
            </div>
            
            <div className="pt-4 border-t border-neutral-100 dark:border-neutral-800 flex justify-center divide-x divide-neutral-100 dark:divide-neutral-800">
              <div className="px-6 text-center">
                <p className="text-xs text-neutral-500 mb-1">Confidence</p>
                <p className="font-mono font-medium">
                  {(result.confidence * 100).toFixed(1)}%
                </p>
              </div>
              <div className="px-6 text-center">
                <p className="text-xs text-neutral-500 mb-1">Model</p>
                <p className="font-mono font-medium">LogReg</p>
              </div>
            </div>

          </div>
        )}

      </div>
    </div>
  )
}

export default App
