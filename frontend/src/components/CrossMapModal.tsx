import React, { useState, useEffect } from 'react';
import { X, Download, Filter, BarChart3 } from 'lucide-react';
import { API_BASE } from '../config';

interface CrossMapEntry {
    nist_id: string;
    nist_title: string;
    nist_family: string;
    iso27001?: string[];
    iso27001_titles?: string[];
    csf2?: string[];
    csf2_titles?: string[];
    iso27005?: string[];
    iso27005_titles?: string[];
}

interface CrossMapStats {
    total_nist_controls: number;
    nist_families: number;
    unique_iso27001_controls: number;
    unique_csf2_categories: number;
    unique_iso27005_clauses: number;
}

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

// API_BASE imported from ../config

const CrossMapModal: React.FC<Props> = ({ isOpen, onClose }) => {
    const [mappings, setMappings] = useState<CrossMapEntry[]>([]);
    const [families, setFamilies] = useState<string[]>([]);
    const [stats, setStats] = useState<CrossMapStats | null>(null);
    const [selectedFamily, setSelectedFamily] = useState<string>('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!isOpen) return;
        setLoading(true);
        Promise.all([
            fetch(`${API_BASE}/api/crossmap`).then(r => r.json()),
            fetch(`${API_BASE}/api/crossmap/families`).then(r => r.json()),
            fetch(`${API_BASE}/api/crossmap/stats`).then(r => r.json()),
        ])
            .then(([mapData, famData, statsData]) => {
                setMappings(mapData.mappings);
                setFamilies(famData.families);
                setStats(statsData);
            })
            .catch(() => { })
            .finally(() => setLoading(false));
    }, [isOpen]);

    useEffect(() => {
        if (!isOpen || !selectedFamily) return;
        setLoading(true);
        const url = selectedFamily
            ? `${API_BASE}/api/crossmap?family=${encodeURIComponent(selectedFamily)}`
            : `${API_BASE}/api/crossmap`;
        fetch(url)
            .then(r => r.json())
            .then(data => setMappings(data.mappings))
            .catch(() => { })
            .finally(() => setLoading(false));
    }, [selectedFamily, isOpen]);

    const handleDownloadCSV = () => {
        window.open(`${API_BASE}/api/crossmap/sankey`, '_blank');
    };

    const handleClearFilter = () => {
        setSelectedFamily('');
        fetch(`${API_BASE}/api/crossmap`)
            .then(r => r.json())
            .then(data => setMappings(data.mappings))
            .catch(() => { });
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[200] flex items-center justify-center">
            <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />
            <div className="relative w-[90vw] max-w-5xl max-h-[85vh] bg-brand-dark border border-white/10 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 shrink-0">
                    <div className="flex items-center gap-3">
                        <BarChart3 className="w-5 h-5 text-brand-purple" />
                        <h2 className="text-lg font-black tracking-tight text-white">Compliance Cross-Mapping</h2>
                        <span className="text-[10px] font-bold uppercase tracking-widest text-gray-500 bg-white/5 px-2 py-0.5 rounded-full">
                            NIST 800-53 &rarr; ISO 27001 &bull; CSF 2.0 &bull; ISO 27005
                        </span>
                    </div>
                    <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-lg transition-colors">
                        <X className="w-4 h-4 text-gray-400" />
                    </button>
                </div>

                {/* Stats Bar */}
                {stats && (
                    <div className="grid grid-cols-5 gap-3 px-6 py-3 border-b border-white/5 shrink-0">
                        <div className="text-center">
                            <div className="text-lg font-black text-brand-cyan">{stats.total_nist_controls}</div>
                            <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider">NIST Controls</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-black text-brand-purple">{stats.nist_families}</div>
                            <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider">Families</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-black text-blue-400">{stats.unique_iso27001_controls}</div>
                            <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider">ISO 27001</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-black text-emerald-400">{stats.unique_csf2_categories}</div>
                            <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider">CSF 2.0</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-black text-amber-400">{stats.unique_iso27005_clauses}</div>
                            <div className="text-[9px] text-gray-500 font-bold uppercase tracking-wider">ISO 27005</div>
                        </div>
                    </div>
                )}

                {/* Filter + Download */}
                <div className="flex items-center gap-3 px-6 py-3 border-b border-white/5 shrink-0">
                    <Filter className="w-4 h-4 text-gray-500" />
                    <select
                        value={selectedFamily}
                        onChange={(e) => setSelectedFamily(e.target.value)}
                        className="bg-white/5 border border-white/10 text-sm text-gray-300 rounded-lg px-3 py-1.5 focus:outline-none focus:border-brand-cyan/50"
                    >
                        <option value="">All Families</option>
                        {families.map(f => (
                            <option key={f} value={f}>{f}</option>
                        ))}
                    </select>
                    {selectedFamily && (
                        <button onClick={handleClearFilter} className="text-[10px] text-brand-cyan hover:underline">
                            Clear filter
                        </button>
                    )}
                    <div className="flex-grow" />
                    <button
                        onClick={handleDownloadCSV}
                        className="flex items-center gap-2 px-3 py-1.5 bg-brand-purple/20 hover:bg-brand-purple/30 border border-brand-purple/30 rounded-lg text-xs font-bold text-brand-purple transition-colors"
                    >
                        <Download className="w-3.5 h-3.5" />
                        Sankey CSV
                    </button>
                </div>

                {/* Table */}
                <div className="flex-grow overflow-auto custom-scrollbar">
                    {loading ? (
                        <div className="flex items-center justify-center h-40 text-gray-500 text-sm">Loading...</div>
                    ) : (
                        <table className="w-full text-xs">
                            <thead className="sticky top-0 bg-brand-dark/95 backdrop-blur-sm border-b border-white/10">
                                <tr>
                                    <th className="text-left px-4 py-3 text-[10px] font-black uppercase tracking-wider text-gray-500">NIST Control</th>
                                    <th className="text-left px-4 py-3 text-[10px] font-black uppercase tracking-wider text-gray-500">Family</th>
                                    <th className="text-left px-4 py-3 text-[10px] font-black uppercase tracking-wider text-blue-400">ISO 27001</th>
                                    <th className="text-left px-4 py-3 text-[10px] font-black uppercase tracking-wider text-emerald-400">CSF 2.0</th>
                                    <th className="text-left px-4 py-3 text-[10px] font-black uppercase tracking-wider text-amber-400">ISO 27005</th>
                                </tr>
                            </thead>
                            <tbody>
                                {mappings.map((entry) => (
                                    <tr key={entry.nist_id} className="border-b border-white/5 hover:bg-white/[0.03] transition-colors">
                                        <td className="px-4 py-3">
                                            <div className="font-bold text-white">{entry.nist_id}</div>
                                            <div className="text-[10px] text-gray-500 mt-0.5">{entry.nist_title}</div>
                                        </td>
                                        <td className="px-4 py-3 text-gray-400">{entry.nist_family}</td>
                                        <td className="px-4 py-3">
                                            {entry.iso27001?.map((ctrl, i) => (
                                                <div key={ctrl} className="mb-1">
                                                    <span className="text-blue-400 font-bold">{ctrl}</span>
                                                    {entry.iso27001_titles?.[i] && (
                                                        <span className="text-gray-500 ml-1">— {entry.iso27001_titles[i]}</span>
                                                    )}
                                                </div>
                                            ))}
                                        </td>
                                        <td className="px-4 py-3">
                                            {entry.csf2?.map((cat, i) => (
                                                <div key={cat} className="mb-1">
                                                    <span className="text-emerald-400 font-bold">{cat}</span>
                                                    {entry.csf2_titles?.[i] && (
                                                        <span className="text-gray-500 ml-1">— {entry.csf2_titles[i]}</span>
                                                    )}
                                                </div>
                                            ))}
                                        </td>
                                        <td className="px-4 py-3">
                                            {entry.iso27005?.map((clause, i) => (
                                                <div key={clause} className="mb-1">
                                                    <span className="text-amber-400 font-bold">{clause}</span>
                                                    {entry.iso27005_titles?.[i] && (
                                                        <span className="text-gray-500 ml-1">— {entry.iso27005_titles[i]}</span>
                                                    )}
                                                </div>
                                            ))}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                {/* Footer */}
                <div className="px-6 py-3 border-t border-white/10 text-[10px] text-gray-500 flex items-center justify-between shrink-0">
                    <span>{mappings.length} mappings shown</span>
                    <span>NIST SP 800-53 Rev.5 &bull; ISO/IEC 27001:2022 &bull; NIST CSF 2.0 &bull; ISO/IEC 27005:2022</span>
                </div>
            </div>
        </div>
    );
};

export default CrossMapModal;
