import pandas as pd 
import numpy as np 
import os 
import matplotlib.pyplot as plt 
import seaborn as sns

def main(threshold=0.0):
    for partition_num in range(0, 10):
        df = pd.read_parquet(f"./jane-street-real-time-market-data-forecasting/train.parquet/partition_id={partition_num}/part-0.parquet")

        feature_columns = df.columns.str.contains('feature')
        responder_columns = df.columns.str.contains('responder')
        target_columns = feature_columns + responder_columns
        
        correlation = df.loc[:, target_columns].corr()
        
        save_dir = './feature_corr'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
                    
        plt.figure(figsize=(60, 40))  
        sns.heatmap(correlation, cmap='coolwarm')
        plt.xticks(rotation=45, fontsize=12)       # x축 레이블
        plt.yticks(rotation=0, fontsize=12)        # y축 레이블
        plt.tight_layout()
        
        plt.savefig(os.path.join(save_dir, f'partition_{partition_num}.png'), 
                            dpi=300, 
                            bbox_inches='tight', 
                            format='png')
        
        high_corr = correlation[abs(correlation) > threshold]
        high_corr = high_corr[high_corr != 1.0]  # 자기 자신과의 상관관계(1.0) 제외

        high_corr_pairs = []
        for i in range(len(correlation.columns)):
            for j in range(i+1, len(correlation.columns)):
                if abs(correlation.iloc[i,j]) > threshold:
                    high_corr_pairs.append({
                        'var1': correlation.columns[i],
                        'var2': correlation.columns[j],
                        'correlation': correlation.iloc[i,j]
                    })

        high_corr_df = pd.DataFrame(high_corr_pairs)
        if not high_corr_df.empty:
            high_corr_df = high_corr_df.sort_values('correlation', ascending=False)
        
        
        csv_save_dir = os.path.join(save_dir, f"{partition_num}.csv")
        high_corr_df.to_csv(csv_save_dir)
        
        plt.close('all')
        print("process complete: ",partition_num)    
        plt.close('all')


if __name__ == '__main__':
    threshold = 0.0
    main(threshold)