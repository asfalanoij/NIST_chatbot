
import React, { useState } from 'react';

const Footer = (): React.ReactNode => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const validateEmail = (email: string) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: { [key: string]: string } = {};

    if (!formData.name.trim()) newErrors.name = 'Identification is required.';
    if (!formData.email.trim()) {
      newErrors.email = 'Electronic mail is required.';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please provide a valid format.';
    }
    if (!formData.message.trim()) newErrors.message = 'Inquiry content is missing.';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsSubmitting(false);
    setIsSuccess(true);
    setFormData({ name: '', email: '', message: '' });

    // Reset success message after 5 seconds
    setTimeout(() => setIsSuccess(false), 5000);
  };

  return (
    <footer id="contact" className="w-full py-24 mt-20 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-[#0B0C10]">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-start">
            
            {/* Left Side: Strategic CTA */}
            <div className="mb-16 md:mb-0 max-w-xl">
                <p className="text-[10px] font-black uppercase tracking-[0.5em] text-[#4AB7C3] mb-4">/ Strategic Dialogue</p>
                <h2 className="text-5xl md:text-7xl font-black text-gray-900 dark:text-white mb-6 tracking-tighter leading-[0.9]">Let's <br className="hidden md:block"/>Connect.</h2>
                <p className="mt-8 text-gray-500 dark:text-gray-400 text-lg leading-relaxed font-serif italic">
                    "Effective governance is the bridge between technological chaos and sustainable resilience."
                </p>
                
                <div className="mt-12 flex items-center gap-10">
                    <div className="relative group cursor-pointer" onClick={handleSubmit}>
                        <div className="w-32 h-32 rounded-full bg-[#5D5CDE] flex items-center justify-center text-center text-[10px] text-white p-4 font-black uppercase tracking-widest leading-tight transition-all duration-700 group-hover:scale-110 group-hover:rotate-12 shadow-[0_20px_50px_rgba(93,92,222,0.3)]">
                            Initiate <br/>Dialogue
                        </div>
                    </div>
                    <div className="space-y-2">
                        <p className="text-xs font-bold text-gray-900 dark:text-white uppercase tracking-widest">Global Reach</p>
                        <p className="text-xs text-gray-500 uppercase tracking-widest">Tokyo | Jakarta | Global Remote</p>
                    </div>
                </div>
            </div>

            {/* Right Side: Professional Outreach */}
            <div className="w-full md:w-1/2 md:pl-20">
                <div className="bg-white dark:bg-[#1E202B] p-10 rounded-[2rem] shadow-2xl border border-gray-200 dark:border-white/5 relative">
                    {isSuccess && (
                      <div className="absolute inset-0 z-50 bg-[#4AB7C3]/90 backdrop-blur-md rounded-[2rem] flex flex-col items-center justify-center text-gray-900 animate-in fade-in duration-500">
                         <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mb-4">
                           <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
                         </div>
                         <h3 className="text-2xl font-black uppercase tracking-tighter">Signal Received</h3>
                         <p className="text-xs font-bold uppercase tracking-widest mt-2">Expect a response within one business cycle.</p>
                      </div>
                    )}

                    <form className="grid grid-cols-1 gap-10" onSubmit={handleSubmit}>
                        <div className={`group border-b pb-4 transition-colors ${errors.name ? 'border-red-500' : 'border-gray-300 dark:border-gray-700 focus-within:border-[#4AB7C3]'}`}>
                            <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.3em] block mb-2">Identify Yourself</label>
                            <input 
                              type="text" 
                              name="name"
                              value={formData.name}
                              onChange={handleInputChange}
                              placeholder="Name or Organization" 
                              className="bg-transparent w-full text-lg font-bold text-gray-900 dark:text-white focus:outline-none placeholder-gray-300 dark:placeholder-gray-700" 
                            />
                            {errors.name && <span className="text-[10px] text-red-500 font-bold uppercase tracking-widest mt-1 block">{errors.name}</span>}
                        </div>
                        <div className={`group border-b pb-4 transition-colors ${errors.email ? 'border-red-500' : 'border-gray-300 dark:border-gray-700 focus-within:border-[#4AB7C3]'}`}>
                            <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.3em] block mb-2">Electronic Mail</label>
                            <input 
                              type="text" 
                              name="email"
                              value={formData.email}
                              onChange={handleInputChange}
                              placeholder="professional@email.com" 
                              className="bg-transparent w-full text-lg font-bold text-gray-900 dark:text-white focus:outline-none placeholder-gray-300 dark:placeholder-gray-700" 
                            />
                            {errors.email && <span className="text-[10px] text-red-500 font-bold uppercase tracking-widest mt-1 block">{errors.email}</span>}
                        </div>
                        <div className={`group border-b pb-4 transition-colors ${errors.message ? 'border-red-500' : 'border-gray-300 dark:border-gray-700 focus-within:border-[#4AB7C3]'}`}>
                            <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.3em] block mb-2">The Inquiry</label>
                            <textarea 
                              name="message"
                              value={formData.message}
                              onChange={handleInputChange}
                              rows={2} 
                              placeholder="Brief context of the engagement..." 
                              className="bg-transparent w-full text-lg font-bold text-gray-900 dark:text-white focus:outline-none placeholder-gray-300 dark:placeholder-gray-700 resize-none" 
                            />
                            {errors.message && <span className="text-[10px] text-red-500 font-bold uppercase tracking-widest mt-1 block">{errors.message}</span>}
                        </div>
                        
                        <button 
                          type="submit"
                          disabled={isSubmitting}
                          className={`bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-black uppercase tracking-[0.4em] text-[10px] py-6 px-10 rounded-full transition-all duration-500 flex items-center justify-between group ${isSubmitting ? 'opacity-50 cursor-not-allowed' : 'hover:bg-[#4AB7C3] dark:hover:bg-[#4AB7C3] dark:hover:text-gray-900'}`}
                        >
                            {isSubmitting ? 'Processing Transmission...' : 'Transmit Signal'}
                            <span className={`text-xl transition-transform ${isSubmitting ? 'animate-pulse' : 'group-hover:translate-x-2'}`}>→</span>
                        </button>
                    </form>
                </div>

                <div className="mt-16 pt-8 border-t border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row items-center justify-between text-[10px] font-black uppercase tracking-[0.3em] text-gray-500">
                    <div>
                        <span className="text-gray-900 dark:text-white">RUDY / P.</span> © 2026 STRATEGIC OVERSIGHT
                    </div>
                    <div className="flex gap-8 mt-6 sm:mt-0">
                        <a href="#" className="hover:text-[#4AB7C3] transition-colors">LinkedIn</a>
                        <a href="#" className="hover:text-[#4AB7C3] transition-colors">Digital Archive</a>
                        <a href="#" className="hover:text-[#4AB7C3] transition-colors">Encrypted Mail</a>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
