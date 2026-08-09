import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Play, Film, Sparkles, X, Clapperboard } from 'lucide-react';

interface VideoItem {
  id: number;
  title: string;
  desc: string;
  video_url: string;
  cover: string;
  tools: string[];
  isVertical?: boolean;
}

export const VideoShowcase: React.FC = () => {
  const { t } = useTranslation();
  const [activeVideo, setActiveVideo] = useState<VideoItem | null>(null);

  const sampleVideos: VideoItem[] = [
    {
      id: 1,
      title: "AI Brand Commercial 9:16 Promo",
      desc: "Futuristic robotic & AI brand commercial generated with Midjourney and Runway Gen-2.",
      video_url: "https://assets.mixkit.co/videos/preview/mixkit-futuristic-robotic-arm-working-41372-large.mp4",
      cover: "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&q=80",
      tools: ["Runway Gen-2", "Midjourney v6", "ElevenLabs AI"],
      isVertical: true
    },
    {
      id: 2,
      title: "Telegram Bot UI & App Demo",
      desc: "Interactive demonstration of high-speed Telegram Mini App & food ordering experience.",
      video_url: "https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-smartphone-with-green-screen-41527-large.mp4",
      cover: "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
      tools: ["Screen Capture", "CapCut", "Framer Motion"],
      isVertical: false
    },
    {
      id: 3,
      title: "AI Product Animation Showcase",
      desc: "Photorealistic 3D AI product presentation and dynamic voiceover generation.",
      video_url: "https://assets.mixkit.co/videos/preview/mixkit-circuit-board-with-glowing-lines-41566-large.mp4",
      cover: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80",
      tools: ["Pika Labs", "Midjourney", "Voiceover AI"],
      isVertical: false
    }
  ];

  return (
    <section id="videos" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full flex items-center justify-center gap-1.5 w-fit mx-auto">
            <Sparkles className="w-3.5 h-3.5" />
            {t('videos.title')}
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            {t('videos.subtitle')}
          </h2>
        </div>

        {/* Video Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {sampleVideos.map((vid, idx) => (
            <motion.div
              key={vid.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="glass-card rounded-2xl overflow-hidden border border-white/10 hover:border-amber-400/40 transition-all flex flex-col group"
            >
              
              {/* Media Thumbnail with Play Overlay */}
              <div 
                onClick={() => setActiveVideo(vid)}
                className={`relative overflow-hidden bg-slate-900 cursor-pointer ${
                  vid.isVertical ? 'aspect-[9/16] max-h-[380px]' : 'aspect-video'
                }`}
              >
                <img
                  src={vid.cover}
                  alt={vid.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                  <div className="w-14 h-14 rounded-full bg-amber-400/90 text-slate-900 flex items-center justify-center group-hover:scale-110 transition-transform shadow-xl shadow-amber-400/30">
                    <Play className="w-6 h-6 fill-current ml-1" />
                  </div>
                </div>

                <span className="absolute bottom-3 left-3 px-2.5 py-1 rounded bg-black/70 text-[10px] font-mono text-amber-400 border border-amber-400/30 flex items-center gap-1">
                  <Clapperboard className="w-3 h-3" /> MP4 Video
                </span>
              </div>

              {/* Description & Tools */}
              <div className="p-6 space-y-4 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="text-lg font-bold text-white group-hover:text-amber-400 transition-colors">
                    {vid.title}
                  </h3>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    {vid.desc}
                  </p>
                </div>

                <div className="flex flex-wrap gap-1.5 pt-2 border-t border-white/10">
                  {vid.tools.map((tool, tIdx) => (
                    <span key={tIdx} className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-400/10 text-amber-300 border border-amber-400/20">
                      {tool}
                    </span>
                  ))}
                </div>
              </div>

            </motion.div>
          ))}
        </div>

        {/* Video Lightbox Modal */}
        {activeVideo && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-lg animate-fadeIn">
            <div className="relative w-full max-w-4xl glass-panel rounded-3xl p-4 sm:p-6 border border-white/20">
              
              <button
                onClick={() => setActiveVideo(null)}
                className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white z-10"
              >
                <X className="w-6 h-6" />
              </button>

              <div className="relative aspect-video rounded-2xl overflow-hidden bg-black flex items-center justify-center">
                <video
                  src={activeVideo.video_url}
                  controls
                  autoPlay
                  className="w-full h-full object-contain"
                />
              </div>

              <div className="mt-4">
                <h3 className="text-xl font-bold text-white">{activeVideo.title}</h3>
                <p className="text-sm text-slate-300 mt-1">{activeVideo.desc}</p>
              </div>

            </div>
          </div>
        )}

      </div>
    </section>
  );
};
