import { Heart, Mail, FileText } from 'lucide-react'

export function Footer() {
  return (
    <footer className="bg-muted/50 border-t border-border mt-auto">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="font-semibold text-lg mb-4">About</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Detect The Stress is a tool designed to help you understand your digital wellbeing through language pattern analysis.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-lg mb-4">Important Notice</h3>
            <p className="text-muted-foreground text-sm leading-relaxed italic">
              This tool provides insights based on language patterns and is not a substitute for professional mental health advice. If you're experiencing mental health concerns, please consult with a qualified healthcare provider.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-lg mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors flex items-center space-x-2">
                  <FileText className="h-4 w-4" />
                  <span>Privacy Policy</span>
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span>Contact Us</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-border pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-muted-foreground text-sm flex items-center space-x-2">
            <span>Made with</span>
            <Heart className="h-4 w-4 text-destructive fill-destructive" />
            <span>for mental health awareness</span>
          </p>
          <p className="text-muted-foreground text-sm mt-4 sm:mt-0">
            © 2024 Detect The Stress. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
