import pandas as pd 
import numpy as np 
import os 
import matplotlib.pyplot as plt 

def main():
    for partition_num in range(8,10):
        df = pd.read_parquet(f"./jane-street-real-time-market-data-forecasting/train.parquet/partition_id={partition_num}/part-0.parquet")


        for symbol in df['symbol_id'].unique():
            target_df = df.loc[df['symbol_id']==symbol]
            
            feature_columns = target_df.columns.str.contains('feature')
            response_columns = target_df.columns.str.contains('responder')
            target_columns = feature_columns + response_columns
            # Figure와 Axes 생성
            fig, axes = plt.subplots(figsize=(50, 40))

            # 히스토그램 그리기
            hist = target_df.loc[:, target_columns].hist(figsize=(50, 40), bins=50)

            # 레이아웃과 레이블 조정
            plt.tight_layout(pad=2.0)

            # 각 subplot에 결측치 개수 표시
            for ax, col in zip(plt.gcf().axes, target_df.loc[:, target_columns].columns):
                # 결측치 개수와 비율 계산
                nan_count = target_df[col].isna().sum()
                nan_ratio = (nan_count / len(target_df)) * 100
                
                # 결측치 정보를 텍스트로 추가
                ax.text(0.95, 0.95, 
                        f'NaN: {nan_count}\n({nan_ratio:.1f}%)',
                        transform=ax.transAxes,
                        horizontalalignment='right',
                        verticalalignment='top',
                        bbox=dict(facecolor='white', alpha=0.8))
                    
                ax.tick_params(axis='x', rotation=45)

            plt.tight_layout(pad=2.0)
            # 저장 디렉토리 확인/생성
            save_dir = './feature_distribution'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            plt.title(f"symbol{symbol}-partition{0}_count-{target_df.shape[0]}")
            # 저장하기 (show 전에)
            plt.savefig(os.path.join(save_dir, f'symbol{symbol}-partition_{partition_num}.png'), 
                        dpi=300, 
                        bbox_inches='tight', 
                        format='png')
            plt.close('all')
            print(f"symbol{symbol}-partition{0}_count-{target_df.shape[0]}")
                
        del target_df
        plt.clf()
        plt.cla()

if __name__ == '__main__':
    main()